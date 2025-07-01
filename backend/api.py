from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import asyncio

from models import (
    GenerateVideoRequest, JobProgress, VideoResult, JobDetails, JobStatus,
    VideoBackend, VideoGenerationOptions, VideoGenerationResult
)
# Removed circular import - agents are imported directly
from agents.video_agent import VideoAgent
from agents.script_agent import ScriptAgent
from agents.voice_agent import VoiceAgent
from agents.editor_agent import EditorAgent

# Initialize FastAPI app
app = FastAPI(
    title="AI Video Generator API",
    description="API for generating narrated videos using CrewAI and multiple AI services",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize video generation crew
crew = VideoGenerationCrew()

# In-memory storage for jobs (replace with database in production)
jobs: Dict[str, JobDetails] = {}

# Initialize agents
script_agent = ScriptAgent()
voice_agent = VoiceAgent()
video_agent = VideoAgent()
editor_agent = EditorAgent()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Video Generator API",
        "version": "2.0.0",
        "features": [
            "Multi-backend video generation",
            "Automatic fallback logic",
            "Real-time progress tracking",
            "Professional voice synthesis"
        ],
        "backends": video_agent.get_available_backends(),
        "endpoints": [
            "/generate - Start video generation",
            "/job/{job_id} - Get job status",
            "/job/{job_id}/result - Get video result",
            "/backends - List available backends",
            "/models - List available models"
        ]
    }

@app.post("/generate")
async def generate_video(request: GenerateVideoRequest, background_tasks: BackgroundTasks):
    """Start video generation with specified backend"""
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Create initial job progress
    progress = JobProgress(
        job_id=job_id,
        status=JobStatus.PENDING,
        progress=0.0,
        current_step="Initializing video generation",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Store job details
    jobs[job_id] = JobDetails(
        job_id=job_id,
        request=request,
        progress=progress
    )
    
    # Start background video generation task
    background_tasks.add_task(process_video_generation, job_id, request)
    
    return {
        "job_id": job_id,
        "status": "started",
        "message": f"Video generation started with {request.backend.value} backend",
        "estimated_time": "2-5 minutes"
    }

@app.get("/job/{job_id}")
async def get_job_status(job_id: str):
    """Get job status and progress"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job.progress.status.value,
        "progress": job.progress.progress,
        "current_step": job.progress.current_step,
        "error_message": job.progress.error_message,
        "created_at": job.progress.created_at,
        "updated_at": job.progress.updated_at,
        "backend": job.request.backend.value
    }

@app.get("/job/{job_id}/result")
async def get_job_result(job_id: str):
    """Get video result when job is completed"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job.progress.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400, 
            detail=f"Job not completed. Current status: {job.progress.status.value}"
        )
    
    if not job.result:
        raise HTTPException(status_code=404, detail="Video result not found")
    
    return {
        "job_id": job_id,
        "video_url": job.result.video_url,
        "thumbnail_url": job.result.thumbnail_url,
        "duration": job.result.duration,
        "file_size": job.result.file_size,
        "created_at": job.result.created_at,
        "backend_used": job.result.backend_used,
        "metadata": job.result.metadata
    }

@app.get("/backends")
async def list_backends():
    """List available video generation backends"""
    backends = video_agent.get_available_backends()
    
    return {
        "available_backends": backends,
        "default": "auto",
        "descriptions": {
            "auto": "Automatic selection with fallback logic",
            "pollo": "Pollo.ai Veo 3 - High quality, cinematic videos",
            "imagineart": "ImagineArt - Fast generation, multiple styles"
        }
    }

@app.get("/models")
async def list_models():
    """List available models from all backends"""
    try:
        models = await video_agent.list_available_models()
        return {
            "models": models,
            "total_backends": len(models),
            "backends": list(models.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

@app.post("/test-backend")
async def test_backend(backend: str, prompt: str = "A beautiful sunset over the ocean"):
    """Test a specific backend with a simple prompt"""
    try:
        result = await video_agent.act(
            prompt=prompt,
            model_name=backend,
            options={"resolution": "720p", "length": 3, "quality": "standard"}
        )
        
        return {
            "backend": backend,
            "success": result.success,
            "video_url": result.video_url if result.success else None,
            "error": result.error_message if not result.success else None,
            "backend_used": result.backend_used
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backend test failed: {str(e)}")

async def process_video_generation(job_id: str, request: GenerateVideoRequest):
    """Background task to process video generation"""
    try:
        job = jobs[job_id]
        
        # Step 1: Generate script
        await update_job_progress(job_id, JobStatus.SCRIPT_GENERATING, 10, "Generating script from prompt")
        
        script = await script_agent.generate_script(
            prompt=request.prompt,
            style=request.style,
            duration=request.duration,
            language=request.language
        )
        
        # Step 2: Generate voice
        await update_job_progress(job_id, JobStatus.VOICE_GENERATING, 30, "Generating voice narration")
        
        voice_segments = await voice_agent.generate_voice_segments(
            script=script,
            voice_style=request.voice_style,
            language=request.language
        )
        
        # Step 3: Generate video with selected backend
        await update_job_progress(job_id, JobStatus.VIDEO_GENERATING, 50, f"Generating video using {request.backend.value} backend")
        
        video_segments = await video_agent.generate_videos(
            script=script,
            style=request.style,
            backend=request.backend,
            options=request.video_options
        )
        
        # Step 4: Edit and combine
        await update_job_progress(job_id, JobStatus.EDITING, 80, "Editing and combining video segments")
        
        final_video = await editor_agent.combine_segments(
            video_segments=video_segments,
            voice_segments=voice_segments,
            script=script
        )
        
        # Step 5: Upload and finalize
        await update_job_progress(job_id, JobStatus.UPLOADING, 95, "Uploading final video")
        
        # Create final result
        result = VideoResult(
            job_id=job_id,
            video_url=final_video.final_video_url,
            thumbnail_url=final_video.thumbnail_url,
            duration=final_video.duration,
            file_size=final_video.file_size,
            created_at=datetime.now(),
            backend_used=request.backend.value,
            metadata={
                "script_segments": len(script.segments),
                "video_segments": len(video_segments),
                "voice_segments": len(voice_segments),
                "generation_options": request.video_options.dict(),
                "style": request.style.value,
                "voice_style": request.voice_style.value
            }
        )
        
        # Update job with result
        job.result = result
        await update_job_progress(job_id, JobStatus.COMPLETED, 100, "Video generation completed successfully")
        
    except Exception as e:
        error_msg = f"Video generation failed: {str(e)}"
        await update_job_progress(job_id, JobStatus.FAILED, 0, error_msg, error_msg)

async def update_job_progress(
    job_id: str, 
    status: JobStatus, 
    progress: float, 
    current_step: str, 
    error_message: Optional[str] = None
):
    """Update job progress in storage"""
    if job_id in jobs:
        job = jobs[job_id]
        job.progress.status = status
        job.progress.progress = progress
        job.progress.current_step = current_step
        job.progress.error_message = error_message
        job.progress.updated_at = datetime.now()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    backends = video_agent.get_available_backends()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "2.0.0",
        "backends_available": len(backends),
        "backends": backends,
        "active_jobs": len([j for j in jobs.values() if j.progress.status not in [JobStatus.COMPLETED, JobStatus.FAILED]])
    }

@app.get("/download/{job_id}")
async def download_video(job_id: str):
    """Download the generated video file"""
    try:
        job_details = crew.get_job_details(job_id)
        if job_details.result is None:
            raise HTTPException(status_code=404, detail="Video not ready")
        
        video_path = job_details.result.video_url
        
        # If it's a local file, serve it
        if os.path.exists(video_path):
            return FileResponse(
                video_path,
                media_type="video/mp4",
                filename=f"video_{job_id}.mp4"
            )
        else:
            # If it's a URL, redirect to it
            return {"video_url": video_path}
            
    except ValueError:
        raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 