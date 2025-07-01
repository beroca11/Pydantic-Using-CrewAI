import os
import asyncio
import httpx
import json
from typing import List, Optional, Dict, Any
from models import VideoSegment, VideoStyle


class ImagineArtAPI:
    """Tool for generating videos using ImagineArt API"""
    
    def __init__(self):
        self.api_key = os.getenv("IMAGINEART_API_KEY")
        if not self.api_key:
            print("Warning: IMAGINEART_API_KEY not found, using mock implementation")
            self.use_mock = True
        else:
            print("Warning: ImagineArt video generation API is not a real service, using mock implementation")
            self.use_mock = True
        
        # Note: api.imagineart.ai doesn't exist - this is a placeholder implementation
        self.base_url = "https://api.imagineart.ai/v1"  # Non-existent domain
        self.headers = {
            "Authorization": f"Bearer {self.api_key or 'mock-key'}",
            "Content-Type": "application/json"
        }
        
        # Initialize mock API for fallback
        self.mock_api = MockImagineArtAPI()
    
    async def generate_video_from_imagineart(
        self, 
        prompt: str, 
        options: Dict[str, Any] = None
    ) -> str:
        """
        Generate video using ImagineArt API (falls back to mock)
        
        Args:
            prompt: Text description for video generation
            options: Additional options like resolution, length, generateAudio
            
        Returns:
            Video URL or task ID for polling
        """
        # Always use mock since the real API doesn't exist
        return await self.mock_api.generate_video_from_imagineart(prompt, options)
    
    async def generate_video_segments(
        self, 
        scene_descriptions: List[str], 
        style: VideoStyle = VideoStyle.REALISTIC,
        duration_per_segment: int = 5,
        options: Dict[str, Any] = None
    ) -> List[VideoSegment]:
        """
        Generate video segments for scene descriptions using ImagineArt (mock)
        
        Args:
            scene_descriptions: List of scene descriptions
            style: Video style to apply
            duration_per_segment: Duration for each segment
            options: Additional generation options
            
        Returns:
            List of VideoSegment objects
        """
        # Always use mock since the real API doesn't exist
        return await self.mock_api.generate_video_segments(
            scene_descriptions, style, duration_per_segment, options
        )
    
    async def get_generation_status(self, task_id: str) -> Dict[str, Any]:
        """Check the status of a video generation task (mock)"""
        return await self.mock_api.get_generation_status(task_id)
    
    async def list_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available video generation models (mock)"""
        return await self.mock_api.list_available_models()


class MockImagineArtAPI:
    """Mock implementation for testing without ImagineArt API key"""
    
    async def generate_video_from_imagineart(
        self, 
        prompt: str, 
        options: Dict[str, Any] = None
    ) -> str:
        """Mock video generation"""
        # Simulate processing time
        await asyncio.sleep(1.0)
        
        # Generate mock video URL
        video_id = hash(prompt) % 10000
        return f"https://mock-imagineart-storage.com/video_{video_id}.mp4"
    
    async def generate_video_segments(
        self, 
        scene_descriptions: List[str], 
        style: VideoStyle = VideoStyle.REALISTIC,
        duration_per_segment: int = 5,
        options: Dict[str, Any] = None
    ) -> List[VideoSegment]:
        """Mock video segments generation"""
        video_segments = []
        current_time = 0.0
        
        for i, description in enumerate(scene_descriptions):
            # Simulate processing time
            await asyncio.sleep(0.7)
            
            # Create mock video URL
            video_url = f"https://mock-imagineart-storage.com/segment_{i}_{style.value}.mp4"
            
            segment = VideoSegment(
                video_url=video_url,
                scene_description=description,
                start_time=current_time,
                end_time=current_time + duration_per_segment,
                duration=duration_per_segment
            )
            
            video_segments.append(segment)
            current_time += duration_per_segment
        
        return video_segments
    
    async def get_generation_status(self, task_id: str) -> Dict[str, Any]:
        """Return mock task status"""
        return {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "video_url": f"https://mock-imagineart-storage.com/{task_id}.mp4"
        }
    
    async def list_available_models(self) -> List[Dict[str, Any]]:
        """Return mock available models"""
        return [
            {"id": "text-to-video-v2", "name": "Text to Video v2", "description": "Latest text-to-video model"},
            {"id": "image-to-video-v1", "name": "Image to Video v1", "description": "Image-to-video generation"},
            {"id": "text-to-video-v1", "name": "Text to Video v1", "description": "Previous generation model"}
        ] 