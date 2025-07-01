from crewai import Agent, Task
from typing import List, Optional
from models import VoiceSegment, VideoSegment, VideoResult
from tools.ffmpeg_utils import FFmpegUtils, MockFFmpegUtils
import os
import tempfile
from datetime import datetime


class EditorAgent:
    """Agent responsible for video editing and final assembly"""
    
    def __init__(self):
        # Initialize FFmpeg utilities (use mock if FFmpeg not available)
        try:
            self.ffmpeg = FFmpegUtils()
        except Exception:
            print("Using mock FFmpeg utilities for testing")
            self.ffmpeg = MockFFmpegUtils()
        
        # Create CrewAI agent
        self.agent = Agent(
            role="Video Editor",
            goal="Merge audio and video segments into a cohesive final video",
            backstory="Expert in video editing and post-production",
            verbose=True,
            allow_delegation=False
        )
    
    def create_editing_task(self, video_segments: List[VideoSegment], voice_segments: List[VoiceSegment]) -> Task:
        """Create a task for video editing"""
        return Task(
            description="Merge video and audio segments into final video",
            agent=self.agent,
            expected_output="Final video file with synchronized audio"
        )
    
    async def edit_video(
        self, 
        video_segments: List[VideoSegment], 
        voice_segments: List[VoiceSegment],
        background_music: Optional[str] = None
    ) -> VideoResult:
        """Edit and merge video segments with audio"""
        try:
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Merge audio and video
            final_video_path = await self.ffmpeg.merge_audio_video(
                video_segments=video_segments,
                voice_segments=voice_segments,
                output_path=output_path,
                background_music=background_music
            )
            
            # Create thumbnail
            thumbnail_path = output_path.replace(".mp4", "_thumb.jpg")
            await self.ffmpeg.create_thumbnail(
                video_path=final_video_path,
                output_path=thumbnail_path,
                time_position=1.0
            )
            
            # Get video duration
            duration = self.ffmpeg.get_video_duration(final_video_path)
            
            # Get file size
            file_size = os.path.getsize(final_video_path) if os.path.exists(final_video_path) else None
            
            # Create video result
            video_result = VideoResult(
                job_id=f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                video_url=final_video_path,
                thumbnail_url=thumbnail_path if os.path.exists(thumbnail_path) else None,
                duration=duration,
                file_size=file_size,
                metadata={
                    "num_video_segments": len(video_segments),
                    "num_voice_segments": len(voice_segments),
                    "background_music": background_music is not None
                },
                created_at=datetime.now()
            )
            
            return video_result
            
        except Exception as e:
            print(f"Error editing video: {e}")
            return self._create_fallback_result()
    
    def _create_fallback_result(self) -> VideoResult:
        """Create fallback video result"""
        return VideoResult(
            job_id=f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            video_url="fallback_video.mp4",
            thumbnail_url=None,
            duration=30.0,
            file_size=None,
            metadata={"fallback": True},
            created_at=datetime.now()
        )
    
    async def compress_video(self, input_path: str, target_size_mb: int = 50) -> str:
        """Compress video to target file size"""
        try:
            output_path = input_path.replace(".mp4", "_compressed.mp4")
            return await self.ffmpeg.compress_video(
                input_path=input_path,
                output_path=output_path,
                target_size_mb=target_size_mb
            )
        except Exception as e:
            print(f"Error compressing video: {e}")
            return input_path  # Return original if compression fails
    
    def cleanup_temp_files(self, video_result: VideoResult):
        """Clean up temporary files"""
        try:
            # Clean up video file if it's temporary
            if video_result.video_url.startswith("/tmp") and os.path.exists(video_result.video_url):
                os.remove(video_result.video_url)
            
            # Clean up thumbnail if it's temporary
            if video_result.thumbnail_url and video_result.thumbnail_url.startswith("/tmp") and os.path.exists(video_result.thumbnail_url):
                os.remove(video_result.thumbnail_url)
                
        except Exception as e:
            print(f"Warning: Could not clean up temp files: {e}") 