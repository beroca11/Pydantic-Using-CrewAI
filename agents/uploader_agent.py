from crewai import Agent, Task
from typing import Optional
from models import VideoResult
import os
import asyncio
from datetime import datetime


class UploaderAgent:
    """Agent responsible for uploading videos to cloud storage"""
    
    def __init__(self):
        # Check for storage configuration
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.aws_bucket = os.getenv("AWS_S3_BUCKET")
        
        # Create CrewAI agent
        self.agent = Agent(
            role="Video Upload Specialist",
            goal="Upload final videos to cloud storage and generate public URLs",
            backstory="Expert in cloud storage and content delivery",
            verbose=True,
            allow_delegation=False
        )
    
    def create_upload_task(self, video_result: VideoResult) -> Task:
        """Create a task for video upload"""
        return Task(
            description="Upload video to cloud storage and generate public URL",
            agent=self.agent,
            expected_output="Public URL for the uploaded video"
        )
    
    async def upload_video(self, video_result: VideoResult) -> str:
        """Upload video to cloud storage"""
        try:
            # Try Supabase first, then AWS S3, then return local path
            if self.supabase_url and self.supabase_key:
                return await self._upload_to_supabase(video_result)
            elif self.aws_bucket:
                return await self._upload_to_s3(video_result)
            else:
                # Return local path if no cloud storage configured
                return video_result.video_url
                
        except Exception as e:
            print(f"Error uploading video: {e}")
            return video_result.video_url  # Return original path as fallback
    
    async def _upload_to_supabase(self, video_result: VideoResult) -> str:
        """Upload video to Supabase storage"""
        try:
            from supabase import create_client, Client
            
            supabase: Client = create_client(self.supabase_url, self.supabase_key)
            
            # Read video file
            with open(video_result.video_url, 'rb') as f:
                video_data = f.read()
            
            # Upload to Supabase storage
            file_name = f"videos/{video_result.job_id}.mp4"
            result = supabase.storage.from_('videos').upload(
                path=file_name,
                file=video_data,
                file_options={"content-type": "video/mp4"}
            )
            
            # Generate public URL
            public_url = supabase.storage.from_('videos').get_public_url(file_name)
            
            # Upload thumbnail if exists
            if video_result.thumbnail_url and os.path.exists(video_result.thumbnail_url):
                with open(video_result.thumbnail_url, 'rb') as f:
                    thumb_data = f.read()
                
                thumb_name = f"thumbnails/{video_result.job_id}.jpg"
                supabase.storage.from_('thumbnails').upload(
                    path=thumb_name,
                    file=thumb_data,
                    file_options={"content-type": "image/jpeg"}
                )
            
            return public_url
            
        except Exception as e:
            print(f"Supabase upload failed: {e}")
            raise
    
    async def _upload_to_s3(self, video_result: VideoResult) -> str:
        """Upload video to AWS S3"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
            
            # Upload video file
            video_key = f"videos/{video_result.job_id}.mp4"
            s3_client.upload_file(
                video_result.video_url,
                self.aws_bucket,
                video_key,
                ExtraArgs={'ContentType': 'video/mp4', 'ACL': 'public-read'}
            )
            
            # Generate public URL
            video_url = f"https://{self.aws_bucket}.s3.amazonaws.com/{video_key}"
            
            # Upload thumbnail if exists
            if video_result.thumbnail_url and os.path.exists(video_result.thumbnail_url):
                thumb_key = f"thumbnails/{video_result.job_id}.jpg"
                s3_client.upload_file(
                    video_result.thumbnail_url,
                    self.aws_bucket,
                    thumb_key,
                    ExtraArgs={'ContentType': 'image/jpeg', 'ACL': 'public-read'}
                )
            
            return video_url
            
        except Exception as e:
            print(f"S3 upload failed: {e}")
            raise
    
    async def delete_video(self, video_url: str) -> bool:
        """Delete video from cloud storage"""
        try:
            if "supabase" in video_url:
                return await self._delete_from_supabase(video_url)
            elif "s3.amazonaws.com" in video_url:
                return await self._delete_from_s3(video_url)
            else:
                # Local file deletion
                if os.path.exists(video_url):
                    os.remove(video_url)
                    return True
                return False
                
        except Exception as e:
            print(f"Error deleting video: {e}")
            return False
    
    async def _delete_from_supabase(self, video_url: str) -> bool:
        """Delete video from Supabase storage"""
        try:
            from supabase import create_client, Client
            
            supabase: Client = create_client(self.supabase_url, self.supabase_key)
            
            # Extract file path from URL
            file_path = video_url.split('/')[-1]
            supabase.storage.from_('videos').remove([f"videos/{file_path}"])
            
            return True
            
        except Exception as e:
            print(f"Supabase deletion failed: {e}")
            return False
    
    async def _delete_from_s3(self, video_url: str) -> bool:
        """Delete video from AWS S3"""
        try:
            import boto3
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
            
            # Extract key from URL
            key = video_url.split(f"{self.aws_bucket}.s3.amazonaws.com/")[-1]
            s3_client.delete_object(Bucket=self.aws_bucket, Key=key)
            
            return True
            
        except Exception as e:
            print(f"S3 deletion failed: {e}")
            return False


# Mock implementation for testing
class MockUploaderAgent:
    """Mock implementation for testing without cloud storage"""
    
    def __init__(self):
        self.agent = Agent(
            role="Mock Upload Specialist",
            goal="Mock video upload for testing",
            backstory="Mock agent for testing purposes",
            verbose=True,
            allow_delegation=False
        )
    
    def create_upload_task(self, video_result: VideoResult) -> Task:
        return Task(
            description="Mock upload task",
            agent=self.agent,
            expected_output="Mock public URL"
        )
    
    async def upload_video(self, video_result: VideoResult) -> str:
        """Return mock public URL"""
        await asyncio.sleep(0.5)  # Simulate upload time
        return f"https://mock-storage.com/videos/{video_result.job_id}.mp4"
    
    async def delete_video(self, video_url: str) -> bool:
        """Mock video deletion"""
        await asyncio.sleep(0.1)
        return True 