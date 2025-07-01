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
            raise ValueError("IMAGINEART_API_KEY not found in environment variables")
        
        self.base_url = "https://api.imagineart.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_video_from_imagineart(
        self, 
        prompt: str, 
        options: Dict[str, Any] = None
    ) -> str:
        """
        Generate video using ImagineArt API
        
        Args:
            prompt: Text description for video generation
            options: Additional options like resolution, length, generateAudio
            
        Returns:
            Video URL or task ID for polling
        """
        if options is None:
            options = {}
        
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "prompt": prompt,
                    "resolution": options.get("resolution", "1080p"),
                    "length": options.get("length", 7),  # seconds
                    "generateAudio": options.get("generateAudio", True),
                    "model": "text-to-video",
                    "quality": "high",
                    "style": options.get("style", "realistic")
                }
                
                response = await client.post(
                    f"{self.base_url}/video/generate",
                    headers=self.headers,
                    json=payload,
                    timeout=300.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"ImagineArt API error: {response.status_code} - {response.text}")
                
                data = response.json()
                # Return video URL directly or task ID for polling
                return data.get("video_url") or data.get("task_id")
                
        except Exception as e:
            raise Exception(f"Failed to generate video with ImagineArt: {str(e)}")
    
    async def generate_video_segments(
        self, 
        scene_descriptions: List[str], 
        style: VideoStyle = VideoStyle.REALISTIC,
        duration_per_segment: int = 5,
        options: Dict[str, Any] = None
    ) -> List[VideoSegment]:
        """
        Generate video segments for scene descriptions using ImagineArt
        
        Args:
            scene_descriptions: List of scene descriptions
            style: Video style to apply
            duration_per_segment: Duration for each segment
            options: Additional generation options
            
        Returns:
            List of VideoSegment objects
        """
        if options is None:
            options = {}
        
        try:
            video_segments = []
            current_time = 0.0
            
            for i, description in enumerate(scene_descriptions):
                # Create style-enhanced prompt
                style_prompt = self._get_style_prompt(style)
                full_prompt = f"{style_prompt} {description}"
                
                # Set up options for this segment
                segment_options = {
                    "resolution": options.get("resolution", "1080p"),
                    "length": duration_per_segment,
                    "generateAudio": options.get("generateAudio", False),  # Usually no audio for segments
                    "style": style.value
                }
                
                # Generate video
                video_url = await self.generate_video_from_imagineart(
                    prompt=full_prompt,
                    options=segment_options
                )
                
                # If we got a task ID instead of URL, poll for completion
                if not video_url.startswith("http"):
                    video_url = await self._poll_for_completion(video_url)
                
                # Create video segment
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
            
        except Exception as e:
            raise Exception(f"Failed to generate video segments with ImagineArt: {str(e)}")
    
    async def _poll_for_completion(self, task_id: str, max_attempts: int = 60) -> str:
        """Poll task status until completion"""
        for attempt in range(max_attempts):
            try:
                status = await self.get_generation_status(task_id)
                
                if status.get("status") == "completed":
                    return status.get("video_url")
                elif status.get("status") == "failed":
                    raise Exception(f"Video generation failed: {status.get('error')}")
                
                # Wait before next poll
                await asyncio.sleep(5)
                
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                await asyncio.sleep(5)
        
        raise Exception("Video generation timed out")
    
    def _get_style_prompt(self, style: VideoStyle) -> str:
        """Get style-specific prompt prefix for ImagineArt"""
        style_prompts = {
            VideoStyle.CINEMATIC: "Cinematic, dramatic lighting, film-like quality, professional cinematography",
            VideoStyle.DOCUMENTARY: "Documentary style, natural lighting, realistic, authentic",
            VideoStyle.ANIMATED: "Animated, cartoon style, vibrant colors, smooth animation",
            VideoStyle.REALISTIC: "Photorealistic, natural, lifelike, high detail",
            VideoStyle.ARTISTIC: "Artistic, stylized, creative, unique visual style"
        }
        return style_prompts.get(style, style_prompts[VideoStyle.REALISTIC])
    
    async def get_generation_status(self, task_id: str) -> Dict[str, Any]:
        """Check the status of a video generation task"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/video/status/{task_id}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get task status: {response.status_code}")
            
            return response.json()
    
    async def list_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available video generation models"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/models",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"Warning: Could not fetch ImagineArt models: {response.status_code}")
                return []
            
            data = response.json()
            return data.get("models", [])


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