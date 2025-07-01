#!/usr/bin/env python3
"""
Pydantic AI Video Generator - Main Entry Point
Enhanced with modular VideoAgent supporting Pollo.ai and ImagineArt backends
"""

import asyncio
import os
import uuid
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api import app as api_app
from models import (
    GenerateVideoRequest, JobProgress, JobStatus, VideoResult, 
    JobDetails, AgentTask, VideoStyle, VoiceStyle, VideoBackend, VideoGenerationOptions, VideoResolution
)
from agents.script_agent import ScriptAgent, MockScriptAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.editor_agent import EditorAgent
from agents.uploader_agent import UploaderAgent, MockUploaderAgent

# Import the demo module
try:
    from demo_video_agent import main as demo_main
except ImportError:
    demo_main = None

class VideoGenerationCrew:
    """Main crew that orchestrates the video generation workflow"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize agents (use mock versions if APIs not available)
        try:
            self.script_agent = ScriptAgent()
        except ValueError:
            print("Using mock script agent")
            self.script_agent = MockScriptAgent()
        
        self.voice_agent = VoiceAgent()
        self.video_agent = VideoAgent()
        self.editor_agent = EditorAgent()
        
        try:
            self.uploader_agent = UploaderAgent()
        except Exception:
            print("Using mock uploader agent")
            self.uploader_agent = MockUploaderAgent()
        
        # Job tracking
        self.jobs: Dict[str, JobDetails] = {}
    
    async def generate_video(self, request: GenerateVideoRequest) -> str:
        """Start video generation workflow"""
        job_id = str(uuid.uuid4())
        
        # Create job progress
        progress = JobProgress(
            job_id=job_id,
            status=JobStatus.PENDING,
            progress=0.0,
            current_step="Initializing",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create job details
        job_details = JobDetails(
            job_id=job_id,
            request=request,
            progress=progress,
            agent_tasks=[]
        )
        
        self.jobs[job_id] = job_details
        
        # Start background task
        asyncio.create_task(self._run_generation_workflow(job_id))
        
        return job_id
    
    async def _run_generation_workflow(self, job_id: str):
        """Run the complete video generation workflow"""
        job = self.jobs[job_id]
        
        try:
            # Step 1: Generate Script
            await self._update_progress(job_id, JobStatus.SCRIPT_GENERATING, 10, "Generating script")
            script = self.script_agent.generate_script(
                prompt=job.request.prompt,
                style=job.request.style,
                voice_style=job.request.voice_style,
                duration=job.request.duration
            )
            
            # Step 2: Generate Voice
            await self._update_progress(job_id, JobStatus.VOICE_GENERATING, 30, "Generating voice narration")
            voice_segments = await self.voice_agent.generate_voice(
                script=script,
                voice_style=job.request.voice_style,
                language=job.request.language
            )
            
            # Step 3: Generate Videos
            await self._update_progress(job_id, JobStatus.VIDEO_GENERATING, 50, "Generating video segments")
            video_segments = await self.video_agent.generate_videos(
                script=script,
                style=job.request.style
            )
            
            # Step 4: Edit and Merge
            await self._update_progress(job_id, JobStatus.EDITING, 80, "Editing final video")
            video_result = await self.editor_agent.edit_video(
                video_segments=video_segments,
                voice_segments=voice_segments
            )
            
            # Step 5: Upload
            await self._update_progress(job_id, JobStatus.UPLOADING, 90, "Uploading video")
            public_url = await self.uploader_agent.upload_video(video_result)
            
            # Update video result with public URL
            video_result.video_url = public_url
            
            # Complete
            await self._update_progress(job_id, JobStatus.COMPLETED, 100, "Video generation completed")
            job.result = video_result
            
            # Cleanup
            self.voice_agent.cleanup_audio_files(voice_segments)
            self.editor_agent.cleanup_temp_files(video_result)
            
        except Exception as e:
            await self._update_progress(
                job_id, 
                JobStatus.FAILED, 
                0, 
                f"Error: {str(e)}"
            )
            print(f"Video generation failed for job {job_id}: {e}")
    
    async def _update_progress(self, job_id: str, status: JobStatus, progress: float, step: str):
        """Update job progress"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.progress.status = status
            job.progress.progress = progress
            job.progress.current_step = step
            job.progress.updated_at = datetime.now()
    
    def get_job_status(self, job_id: str) -> JobProgress:
        """Get current job status"""
        if job_id in self.jobs:
            return self.jobs[job_id].progress
        else:
            raise ValueError(f"Job {job_id} not found")
    
    def get_job_details(self, job_id: str) -> JobDetails:
        """Get complete job details"""
        if job_id in self.jobs:
            return self.jobs[job_id]
        else:
            raise ValueError(f"Job {job_id} not found")
    
    def list_jobs(self) -> Dict[str, JobProgress]:
        """List all jobs"""
        return {job_id: job.progress for job_id, job in self.jobs.items()}

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Pydantic AI Video Generator",
        description="AI-powered video generation with multiple backend support",
        version="2.0.0"
    )
    
    # Mount the API routes
    app.mount("/api", api_app)
    
    # Serve static files (frontend)
    if os.path.exists("frontend/dist"):
        app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
        
        @app.get("/")
        async def serve_frontend():
            return FileResponse("frontend/dist/index.html")
    
    return app

async def test_video_agent():
    """Test the modular video agent system"""
    print("🚀 Testing Modular VideoAgent System")
    print("=" * 50)
    
    try:
        # Initialize the agent
        agent = VideoAgent()
        
        # Display available backends
        backends = agent.get_available_backends()
        print(f"📱 Available backends: {', '.join(backends)}")
        
        # Test basic video generation
        prompt = "A peaceful sunset over the ocean with gentle waves"
        print(f"\n🎬 Generating video: {prompt}")
        
        # Test with auto backend selection
        result = await agent.act(
            prompt=prompt,
            model_name="auto",
            options={
                "resolution": "1080p",
                "length": 5,
                "generateAudio": True,
                "quality": "high"
            }
        )
        
        if result.success:
            print(f"✅ Video generated successfully!")
            print(f"   Backend used: {result.backend_used}")
            print(f"   Video URL: {result.video_url}")
        else:
            print(f"❌ Video generation failed: {result.error_message}")
        
        # Test available models
        print(f"\n🔍 Fetching available models...")
        models = await agent.list_available_models()
        
        for backend, model_list in models.items():
            print(f"   {backend.upper()}: {len(model_list)} models available")
        
        print("\n✅ VideoAgent test completed!")
        
    except Exception as e:
        print(f"❌ VideoAgent test failed: {str(e)}")

async def main():
    """Main entry point with options for different modes"""
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "demo" and demo_main:
            print("🎬 Running comprehensive VideoAgent demo...")
            await demo_main()
            return
        elif mode == "test":
            print("🧪 Running quick VideoAgent test...")
            await test_video_agent()
            return
        elif mode == "server":
            print("🚀 Starting web server...")
        elif mode == "help":
            print("🔧 Pydantic AI Video Generator")
            print("\nUsage:")
            print("  python main.py demo    - Run comprehensive backend demo")
            print("  python main.py test    - Run quick agent test")
            print("  python main.py server  - Start web server")
            print("  python main.py help    - Show this help")
            print("\nEnvironment variables:")
            print("  POLLO_API_KEY         - Pollo.ai API key")
            print("  IMAGINEART_API_KEY    - ImagineArt API key")
            print("  ELEVENLABS_API_KEY    - ElevenLabs API key")
            return
    
    # Default: Start the web server
    print("🌟 Starting Pydantic AI Video Generator")
    print("🔧 Features:")
    print("   • Multi-backend video generation (Pollo.ai + ImagineArt)")
    print("   • Automatic fallback logic")
    print("   • Professional voice synthesis")
    print("   • Real-time progress tracking")
    
    # Quick agent initialization test
    try:
        print("\n🧪 Initializing VideoAgent...")
        agent = VideoAgent()
        backends = agent.get_available_backends()
        print(f"   ✅ Available backends: {', '.join(backends)}")
    except Exception as e:
        print(f"   ⚠️  VideoAgent initialization warning: {str(e)}")
    
    # Create and run the FastAPI app
    app = create_app()
    
    print(f"\n🚀 Server starting at http://localhost:8000")
    print(f"📱 Frontend available at http://localhost:3000")
    print(f"📚 API docs at http://localhost:8000/docs")
    
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {str(e)}") 