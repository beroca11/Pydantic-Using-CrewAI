import os
import asyncio
import httpx
import json
from typing import List, Optional, Dict, Any
from models import VideoSegment, VideoStyle


class PolloVeo3API:
    """Tool for generating videos using Pollo.ai Veo 3 API"""
    
    def __init__(self):
        self.api_key = os.getenv("POLLO_API_KEY")
        if not self.api_key:
            raise ValueError("POLLO_API_KEY not found in environment variables")
        
        self.base_url = "https://api.pollo.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_video_segments(
        self, 
        scene_descriptions: List[str], 
        style: VideoStyle = VideoStyle.CINEMATIC,
        duration_per_segment: int = 5
    ) -> List[VideoSegment]:
        """
        Generate video segments for scene descriptions
        
        Args:
            scene_descriptions: List of scene descriptions to generate videos for
            style: Video style to apply
            duration_per_segment: Duration for each video segment in seconds
            
        Returns:
            List of VideoSegment objects with video URLs and timing
        """
        try:
            video_segments = []
            current_time = 0.0
            
            for i, description in enumerate(scene_descriptions):
                # Create prompt based on style
                style_prompt = self._get_style_prompt(style)
                full_prompt = f"{style_prompt} {description}"
                
                # Generate video using Pollo.ai API
                video_url = await self._generate_video(
                    prompt=full_prompt,
                    duration=duration_per_segment
                )
                
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
            raise Exception(f"Failed to generate video segments: {str(e)}")
    
    async def _generate_video(self, prompt: str, duration: int) -> str:
        """Generate a single video using Pollo.ai API"""
        async with httpx.AsyncClient() as client:
            payload = {
                "prompt": prompt,
                "duration": duration,
                "model": "veo-3",
                "aspect_ratio": "16:9",
                "quality": "high"
            }
            
            response = await client.post(
                f"{self.base_url}/videos/generate",
                headers=self.headers,
                json=payload,
                timeout=300.0  # 5 minutes timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Pollo.ai API error: {response.status_code} - {response.text}")
            
            data = response.json()
            return data.get("video_url")
    
    def _get_style_prompt(self, style: VideoStyle) -> str:
        """Get style-specific prompt prefix"""
        style_prompts = {
            VideoStyle.CINEMATIC: "Cinematic shot, professional lighting, high quality, smooth camera movement",
            VideoStyle.DOCUMENTARY: "Documentary style, natural lighting, realistic, handheld camera",
            VideoStyle.ANIMATED: "Animated style, colorful, smooth animation, artistic",
            VideoStyle.REALISTIC: "Realistic, natural, everyday scene, authentic",
            VideoStyle.ARTISTIC: "Artistic, creative, stylized, visually striking"
        }
        return style_prompts.get(style, style_prompts[VideoStyle.CINEMATIC])
    
    async def get_generation_status(self, job_id: str) -> Dict[str, Any]:
        """Check the status of a video generation job"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/videos/{job_id}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get job status: {response.status_code}")
            
            return response.json()
    
    async def list_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available video generation models"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/models",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"Warning: Could not fetch models: {response.status_code}")
                return []
            
            data = response.json()
            return data.get("models", [])


# Mock implementation for testing without API key
class MockPolloVeo3API:
    """Mock implementation for testing without Pollo.ai API key"""
    
    async def generate_video_segments(
        self, 
        scene_descriptions: List[str], 
        style: VideoStyle = VideoStyle.CINEMATIC,
        duration_per_segment: int = 5
    ) -> List[VideoSegment]:
        """Mock video generation that returns placeholder segments"""
        video_segments = []
        current_time = 0.0
        
        for i, description in enumerate(scene_descriptions):
            # Simulate processing time
            await asyncio.sleep(0.5)
            
            # Create mock video URL
            video_url = f"https://mock-video-storage.com/video_segment_{i}.mp4"
            
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
    
    async def get_generation_status(self, job_id: str) -> Dict[str, Any]:
        """Return mock job status"""
        return {
            "job_id": job_id,
            "status": "completed",
            "progress": 100,
            "video_url": f"https://mock-video-storage.com/{job_id}.mp4"
        }
    
    async def list_available_models(self) -> List[Dict[str, Any]]:
        """Return mock available models"""
        return [
            {"id": "veo-3", "name": "Veo 3", "description": "Latest video generation model"},
            {"id": "veo-2", "name": "Veo 2", "description": "Previous generation model"}
        ] 