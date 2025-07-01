from crewai import Agent, Task
from typing import List, Optional, Dict, Any
from models import (
    VideoSegment, VideoStyle, GeneratedScript, VideoBackend, 
    VideoGenerationOptions, VideoGenerationResult
)
from tools.pollo_veo3_api import PolloVeo3API, MockPolloVeo3API
from tools.imagineart_api import ImagineArtAPI, MockImagineArtAPI
import os
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoAgent:
    """Agent responsible for generating video content with dynamic backend selection"""
    
    def __init__(self):
        # Initialize available APIs
        self.pollo_api = None
        self.imagineart_api = None
        self.available_backends = []
        
        # Try to initialize Pollo.ai API
        try:
            self.pollo_api = PolloVeo3API()
            self.available_backends.append(VideoBackend.POLLO)
            logger.info("Pollo.ai API initialized successfully")
        except ValueError:
            logger.warning("Pollo.ai API key not found, using mock API")
            self.pollo_api = MockPolloVeo3API()
        
        # Try to initialize ImagineArt API
        try:
            self.imagineart_api = ImagineArtAPI()
            self.available_backends.append(VideoBackend.IMAGINEART)
            logger.info("ImagineArt API initialized successfully")
        except ValueError:
            logger.warning("ImagineArt API key not found, using mock API")
            self.imagineart_api = MockImagineArtAPI()
        
        # If no real APIs available, add them to available backends anyway for mock testing
        if not self.available_backends:
            self.available_backends = [VideoBackend.POLLO, VideoBackend.IMAGINEART]
            logger.info("Using mock APIs for both backends")
        
        # Create CrewAI agent
        self.agent = Agent(
            role="Multi-Backend Video Content Creator",
            goal="Generate high-quality video segments using the best available backend",
            backstory="Expert in AI video generation with access to multiple video generation APIs",
            verbose=True,
            allow_delegation=False
        )
    
    def create_video_task(self, script: GeneratedScript, style: VideoStyle, backend: VideoBackend = VideoBackend.AUTO) -> Task:
        """Create a task for video generation with specified backend"""
        backend_info = f" using {backend.value} backend" if backend != VideoBackend.AUTO else " with automatic backend selection"
        
        return Task(
            description=f"Generate video segments for script in {style.value} style{backend_info}",
            agent=self.agent,
            expected_output="Video segments with URLs, timing, and backend information"
        )
    
    async def act(self, prompt: str, model_name: str = "auto", options: Optional[Dict[str, Any]] = None) -> VideoGenerationResult:
        """
        Main entry point for video generation with dynamic backend selection
        
        Args:
            prompt: Video description prompt
            model_name: Backend to use ("pollo", "imagineart", or "auto")
            options: Additional generation options
            
        Returns:
            VideoGenerationResult with video URL and metadata
        """
        try:
            # Normalize model name to backend enum
            backend = self._normalize_backend(model_name)
            
            # Set up generation options
            gen_options = VideoGenerationOptions(**(options or {}))
            
            logger.info(f"Starting video generation with backend: {backend.value}")
            
            # Generate video with specified or automatic backend
            if backend == VideoBackend.AUTO:
                result = await self._generate_with_auto_backend(prompt, gen_options)
            else:
                result = await self._generate_with_backend(prompt, backend, gen_options)
            
            return result
            
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            return VideoGenerationResult(
                success=False,
                backend_used="none",
                error_message=str(e)
            )
    
    async def generate_videos(self, script: GeneratedScript, style: VideoStyle, backend: VideoBackend = VideoBackend.AUTO, options: Optional[VideoGenerationOptions] = None) -> List[VideoSegment]:
        """Generate video segments for script scenes with dynamic backend selection"""
        try:
            if options is None:
                options = VideoGenerationOptions()
            
            # Extract scene descriptions from script segments
            scene_descriptions = []
            for segment in script.segments:
                if segment.scene_description:
                    scene_descriptions.append(segment.scene_description)
                else:
                    # Create scene description from text if none provided
                    scene_desc = f"Scene showing: {segment.text[:50]}..."
                    scene_descriptions.append(scene_desc)
            
            # Calculate duration per segment
            total_duration = script.total_duration
            num_segments = len(scene_descriptions)
            duration_per_segment = max(3, int(total_duration / num_segments))
            
            # Choose backend
            chosen_backend = await self._choose_backend(backend)
            api = self._get_api_for_backend(chosen_backend)
            
            logger.info(f"Generating {num_segments} video segments using {chosen_backend.value}")
            
            # Generate videos using chosen backend
            if chosen_backend == VideoBackend.POLLO:
                # Pollo API doesn't accept options parameter
                video_segments = await api.generate_video_segments(
                    scene_descriptions=scene_descriptions,
                    style=style,
                    duration_per_segment=duration_per_segment
                )
            else:
                # ImagineArt API accepts options parameter
                video_segments = await api.generate_video_segments(
                    scene_descriptions=scene_descriptions,
                    style=style,
                    duration_per_segment=duration_per_segment,
                    options=options.dict() if hasattr(options, 'dict') else options.__dict__
                )
            
            # Add backend information to segments
            for segment in video_segments:
                segment.backend_used = chosen_backend.value
            
            return video_segments
            
        except Exception as e:
            logger.error(f"Error generating videos: {e}")
            # Try fallback if auto mode and primary backend failed
            if backend == VideoBackend.AUTO:
                return await self._generate_with_fallback(script, style, options)
            else:
                return self._create_fallback_videos(script, style)
    
    async def _generate_with_auto_backend(self, prompt: str, options: VideoGenerationOptions) -> VideoGenerationResult:
        """Generate video with automatic backend selection and fallback"""
        # Try Pollo.ai first (preferred for quality)
        try:
            if VideoBackend.POLLO in self.available_backends:
                logger.info("Trying Pollo.ai backend first")
                result = await self._generate_with_backend(prompt, VideoBackend.POLLO, options)
                if result.success:
                    return result
        except Exception as e:
            logger.warning(f"Pollo.ai backend failed: {str(e)}")
        
        # Fallback to ImagineArt
        try:
            if VideoBackend.IMAGINEART in self.available_backends:
                logger.info("Falling back to ImagineArt backend")
                result = await self._generate_with_backend(prompt, VideoBackend.IMAGINEART, options)
                if result.success:
                    return result
        except Exception as e:
            logger.warning(f"ImagineArt backend failed: {str(e)}")
        
        # If both fail, return error
        return VideoGenerationResult(
            success=False,
            backend_used="none",
            error_message="All backends failed"
        )
    
    async def _generate_with_backend(self, prompt: str, backend: VideoBackend, options: VideoGenerationOptions) -> VideoGenerationResult:
        """Generate video using specific backend"""
        try:
            api = self._get_api_for_backend(backend)
            
            # Convert options to dict for API call
            api_options = {
                "resolution": options.resolution.value,
                "length": options.length,
                "generateAudio": options.generateAudio,
                "quality": options.quality
            }
            
            # Generate video
            video_url = await api.generate_video_from_imagineart(prompt, api_options) if backend == VideoBackend.IMAGINEART else await self._generate_with_pollo(prompt, api_options)
            
            return VideoGenerationResult(
                success=True,
                video_url=video_url,
                backend_used=backend.value,
                metadata={"options": api_options}
            )
            
        except Exception as e:
            return VideoGenerationResult(
                success=False,
                backend_used=backend.value,
                error_message=str(e)
            )
    
    async def _generate_with_pollo(self, prompt: str, options: Dict[str, Any]) -> str:
        """Generate video using Pollo.ai API (adapter method)"""
        # Since Pollo doesn't have the same interface, we use the existing method
        video_segments = await self.pollo_api.generate_video_segments(
            scene_descriptions=[prompt],
            duration_per_segment=options.get("length", 7)
        )
        
        if video_segments:
            return video_segments[0].video_url
        else:
            raise Exception("No video generated")
    
    async def _generate_with_fallback(self, script: GeneratedScript, style: VideoStyle, options: Optional[VideoGenerationOptions]) -> List[VideoSegment]:
        """Generate videos with fallback logic"""
        try:
            # Try with alternative backend
            alternative_backend = VideoBackend.IMAGINEART if VideoBackend.POLLO in self.available_backends else VideoBackend.POLLO
            return await self.generate_videos(script, style, alternative_backend, options)
        except Exception:
            # Final fallback to mock videos
            return self._create_fallback_videos(script, style)
    
    async def _choose_backend(self, requested_backend: VideoBackend) -> VideoBackend:
        """Choose the best available backend"""
        if requested_backend != VideoBackend.AUTO:
            return requested_backend
        
        # Auto selection logic: prefer Pollo for quality, ImagineArt for speed
        if VideoBackend.POLLO in self.available_backends:
            return VideoBackend.POLLO
        elif VideoBackend.IMAGINEART in self.available_backends:
            return VideoBackend.IMAGINEART
        else:
            # Fallback to first available (mock)
            return self.available_backends[0] if self.available_backends else VideoBackend.POLLO
    
    def _get_api_for_backend(self, backend: VideoBackend):
        """Get API instance for specified backend"""
        if backend == VideoBackend.POLLO:
            return self.pollo_api
        elif backend == VideoBackend.IMAGINEART:
            return self.imagineart_api
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    def _normalize_backend(self, model_name: str) -> VideoBackend:
        """Normalize model name string to VideoBackend enum"""
        model_name = model_name.lower()
        
        if model_name in ["pollo", "pollo.ai", "veo", "veo3"]:
            return VideoBackend.POLLO
        elif model_name in ["imagineart", "imagine", "imagine-art"]:
            return VideoBackend.IMAGINEART
        else:
            return VideoBackend.AUTO
    
    def _create_fallback_videos(self, script: GeneratedScript, style: VideoStyle) -> List[VideoSegment]:
        """Create fallback video segments when all backends fail"""
        video_segments = []
        current_time = 0.0
        
        for i, segment in enumerate(script.segments):
            # Calculate duration for this segment
            duration = segment.end_time - segment.start_time
            
            video_segment = VideoSegment(
                video_url=f"fallback_video_{i}.mp4",
                scene_description=segment.scene_description or f"Scene {i + 1}",
                start_time=current_time,
                end_time=current_time + duration,
                duration=duration,
                backend_used="fallback"
            )
            
            video_segments.append(video_segment)
            current_time += duration
        
        return video_segments
    
    async def get_generation_status(self, job_id: str, backend: VideoBackend = VideoBackend.AUTO):
        """Check video generation status with specified backend"""
        api = self._get_api_for_backend(backend) if backend != VideoBackend.AUTO else self.pollo_api
        return await api.get_generation_status(job_id)
    
    async def list_available_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get available models from all backends"""
        models = {}
        
        if self.pollo_api:
            try:
                pollo_models = await self.pollo_api.list_available_models()
                models["pollo"] = pollo_models
            except Exception as e:
                logger.warning(f"Could not fetch Pollo models: {e}")
                models["pollo"] = []
        
        if self.imagineart_api:
            try:
                imagineart_models = await self.imagineart_api.list_available_models()
                models["imagineart"] = imagineart_models
            except Exception as e:
                logger.warning(f"Could not fetch ImagineArt models: {e}")
                models["imagineart"] = []
        
        return models
    
    def get_available_backends(self) -> List[str]:
        """Get list of available backends"""
        return [backend.value for backend in self.available_backends] 