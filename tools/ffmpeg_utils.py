import os
import asyncio
import subprocess
import tempfile
from typing import List, Optional, Tuple

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: MoviePy not available: {e}")
    MOVIEPY_AVAILABLE = False
    # Mock classes for when MoviePy is not available
    class VideoFileClip:
        def __init__(self, *args, **kwargs): pass
        def close(self): pass
    class AudioFileClip:
        def __init__(self, *args, **kwargs): pass
        def close(self): pass
    class CompositeVideoClip:
        def __init__(self, *args, **kwargs): pass
        def close(self): pass
    def concatenate_videoclips(*args, **kwargs): 
        return VideoFileClip()

from models import VoiceSegment, VideoSegment


class FFmpegUtils:
    """Utility class for video editing using FFmpeg and MoviePy"""
    
    def __init__(self):
        # Check if FFmpeg is available
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            self.ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.ffmpeg_available = False
            print("Warning: FFmpeg not found. Some features may not work.")
    
    async def merge_audio_video(
        self,
        video_segments: List[VideoSegment],
        voice_segments: List[VoiceSegment],
        output_path: str,
        background_music: Optional[str] = None
    ) -> str:
        """
        Merge video segments with voice narration
        
        Args:
            video_segments: List of video segments
            voice_segments: List of voice segments
            output_path: Path for the final video
            background_music: Optional background music file path
            
        Returns:
            Path to the final merged video
        """
        try:
            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Process video segments
                video_clips = []
                for i, segment in enumerate(video_segments):
                    # Download or copy video file to temp directory
                    temp_video_path = os.path.join(temp_dir, f"video_{i}.mp4")
                    await self._download_file(segment.video_url, temp_video_path)
                    
                    # Load video clip
                    video_clip = VideoFileClip(temp_video_path)
                    video_clips.append(video_clip)
                
                # Process audio segments
                audio_clips = []
                for i, segment in enumerate(voice_segments):
                    # Download or copy audio file to temp directory
                    temp_audio_path = os.path.join(temp_dir, f"audio_{i}.mp3")
                    await self._download_file(segment.audio_url, temp_audio_path)
                    
                    # Load audio clip
                    audio_clip = AudioFileClip(temp_audio_path)
                    audio_clips.append(audio_clip)
                
                # Concatenate video clips
                final_video = concatenate_videoclips(video_clips)
                
                # Concatenate audio clips
                final_audio = concatenate_videoclips(audio_clips)
                
                # Add background music if provided
                if background_music and os.path.exists(background_music):
                    bg_music = AudioFileClip(background_music)
                    # Loop background music to match video duration
                    if bg_music.duration < final_video.duration:
                        loops_needed = int(final_video.duration / bg_music.duration) + 1
                        bg_music = concatenate_videoclips([bg_music] * loops_needed)
                    
                    # Trim to video duration
                    bg_music = bg_music.subclip(0, final_video.duration)
                    
                    # Mix audio (voice + background music at lower volume)
                    bg_music = bg_music.volumex(0.3)  # Reduce background music volume
                    final_audio = final_audio.volumex(1.0)  # Keep voice at full volume
                    mixed_audio = CompositeVideoClip([final_audio, bg_music])
                else:
                    mixed_audio = final_audio
                
                # Set audio to video
                final_video = final_video.set_audio(mixed_audio)
                
                # Write final video
                final_video.write_videofile(
                    output_path,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile=os.path.join(temp_dir, "temp-audio.m4a"),
                    remove_temp=True
                )
                
                # Clean up
                final_video.close()
                mixed_audio.close()
                for clip in video_clips + audio_clips:
                    clip.close()
                
                return output_path
                
        except Exception as e:
            raise Exception(f"Failed to merge audio and video: {str(e)}")
    
    async def create_thumbnail(self, video_path: str, output_path: str, time_position: float = 1.0) -> str:
        """Create a thumbnail from video at specified time position"""
        try:
            if self.ffmpeg_available:
                # Use FFmpeg for thumbnail generation
                cmd = [
                    "ffmpeg", "-i", video_path,
                    "-ss", str(time_position),
                    "-vframes", "1",
                    "-q:v", "2",
                    output_path,
                    "-y"
                ]
                
                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await result.communicate()
                
                if result.returncode != 0:
                    raise Exception("FFmpeg thumbnail generation failed")
                
                return output_path
            else:
                # Fallback to MoviePy
                video = VideoFileClip(video_path)
                frame = video.get_frame(time_position)
                
                from PIL import Image
                import numpy as np
                
                img = Image.fromarray(np.uint8(frame * 255))
                img.save(output_path)
                video.close()
                
                return output_path
                
        except Exception as e:
            raise Exception(f"Failed to create thumbnail: {str(e)}")
    
    async def compress_video(self, input_path: str, output_path: str, target_size_mb: int = 50) -> str:
        """Compress video to target file size"""
        try:
            if not self.ffmpeg_available:
                raise Exception("FFmpeg required for video compression")
            
            # Calculate target bitrate based on file size
            video_info = await self._get_video_info(input_path)
            duration = video_info.get('duration', 60)
            target_bitrate = int((target_size_mb * 8 * 1024 * 1024) / duration)  # bits per second
            
            cmd = [
                "ffmpeg", "-i", input_path,
                "-c:v", "libx264",
                "-b:v", f"{target_bitrate}",
                "-c:a", "aac",
                "-b:a", "128k",
                output_path,
                "-y"
            ]
            
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await result.communicate()
            
            if result.returncode != 0:
                raise Exception("Video compression failed")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to compress video: {str(e)}")
    
    async def _download_file(self, url: str, local_path: str) -> None:
        """Download file from URL or copy local file"""
        if url.startswith(('http://', 'https://')):
            # Download from URL
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
        else:
            # Copy local file
            import shutil
            shutil.copy2(url, local_path)
    
    async def _get_video_info(self, video_path: str) -> dict:
        """Get video information using FFmpeg"""
        if not self.ffmpeg_available:
            return {"duration": 60}  # Default fallback
        
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await result.communicate()
        
        if result.returncode != 0:
            return {"duration": 60}
        
        import json
        info = json.loads(stdout.decode())
        
        # Extract duration
        duration = float(info.get('format', {}).get('duration', 60))
        
        return {
            "duration": duration,
            "format": info.get('format', {}),
            "streams": info.get('streams', [])
        }
    
    def get_video_duration(self, video_path: str) -> float:
        """Get video duration using MoviePy"""
        try:
            video = VideoFileClip(video_path)
            duration = video.duration
            video.close()
            return duration
        except Exception as e:
            print(f"Warning: Could not get video duration: {e}")
            return 60.0  # Default fallback


# Mock implementation for testing
class MockFFmpegUtils:
    """Mock implementation for testing without FFmpeg"""
    
    async def merge_audio_video(
        self,
        video_segments: List[VideoSegment],
        voice_segments: List[VoiceSegment],
        output_path: str,
        background_music: Optional[str] = None
    ) -> str:
        """Mock video merging that creates a placeholder file"""
        # Create a mock output file
        with open(output_path, 'w') as f:
            f.write("Mock video content")
        
        # Simulate processing time
        await asyncio.sleep(1.0)
        
        return output_path
    
    async def create_thumbnail(self, video_path: str, output_path: str, time_position: float = 1.0) -> str:
        """Mock thumbnail creation"""
        # Create a mock thumbnail file
        with open(output_path, 'w') as f:
            f.write("Mock thumbnail")
        
        await asyncio.sleep(0.5)
        return output_path
    
    async def compress_video(self, input_path: str, output_path: str, target_size_mb: int = 50) -> str:
        """Mock video compression"""
        # Copy input to output (mock compression)
        import shutil
        shutil.copy2(input_path, output_path)
        
        await asyncio.sleep(0.5)
        return output_path
    
    def get_video_duration(self, video_path: str) -> float:
        """Mock video duration"""
        return 30.0 