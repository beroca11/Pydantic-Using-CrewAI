from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    PENDING = "pending"
    SCRIPT_GENERATING = "script_generating"
    VOICE_GENERATING = "voice_generating"
    VIDEO_GENERATING = "video_generating"
    EDITING = "editing"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoStyle(str, Enum):
    CINEMATIC = "cinematic"
    DOCUMENTARY = "documentary"
    ANIMATED = "animated"
    REALISTIC = "realistic"
    ARTISTIC = "artistic"


class VoiceStyle(str, Enum):
    NARRATIVE = "narrative"
    CONVERSATIONAL = "conversational"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    DRAMATIC = "dramatic"


class VideoBackend(str, Enum):
    POLLO = "pollo"
    IMAGINEART = "imagineart"
    AUTO = "auto"  # Try preferred, fallback to alternative


class VideoResolution(str, Enum):
    HD_720P = "720p"
    FULL_HD_1080P = "1080p"
    UHD_4K = "4k"


class VideoGenerationOptions(BaseModel):
    """Options for video generation across different backends"""
    resolution: VideoResolution = Field(default=VideoResolution.FULL_HD_1080P, description="Video resolution")
    length: int = Field(default=7, ge=3, le=10, description="Video length in seconds")
    generateAudio: bool = Field(default=True, description="Whether to generate audio")
    quality: str = Field(default="high", description="Video quality setting")
    style_strength: float = Field(default=1.0, ge=0.1, le=2.0, description="Style application strength")


class GenerateVideoRequest(BaseModel):
    prompt: str = Field(..., description="User's video generation prompt")
    style: VideoStyle = Field(default=VideoStyle.CINEMATIC, description="Video style")
    voice_style: VoiceStyle = Field(default=VoiceStyle.NARRATIVE, description="Voice style")
    duration: int = Field(default=30, ge=10, le=120, description="Video duration in seconds")
    language: str = Field(default="en", description="Language for voice generation")
    backend: VideoBackend = Field(default=VideoBackend.AUTO, description="Video generation backend")
    video_options: VideoGenerationOptions = Field(default_factory=VideoGenerationOptions, description="Video generation options")


class ScriptSegment(BaseModel):
    text: str
    start_time: float
    end_time: float
    scene_description: Optional[str] = None


class GeneratedScript(BaseModel):
    title: str
    segments: List[ScriptSegment]
    total_duration: float
    summary: str


class VoiceSegment(BaseModel):
    audio_url: str
    text: str
    start_time: float
    end_time: float
    duration: float


class VideoSegment(BaseModel):
    video_url: str
    scene_description: str
    start_time: float
    end_time: float
    duration: float
    backend_used: Optional[str] = None  # Track which backend generated this segment


class JobProgress(BaseModel):
    job_id: str
    status: JobStatus
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    current_step: str
    estimated_completion: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class VideoResult(BaseModel):
    job_id: str
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: float
    file_size: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    backend_used: Optional[str] = None  # Track which backend was used


class AgentTask(BaseModel):
    task_id: str
    agent_name: str
    status: JobStatus
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None


class JobDetails(BaseModel):
    job_id: str
    request: GenerateVideoRequest
    progress: JobProgress
    result: Optional[VideoResult] = None
    agent_tasks: List[AgentTask] = Field(default_factory=list)


class VideoGenerationResult(BaseModel):
    """Result from video generation with backend tracking"""
    success: bool
    video_url: Optional[str] = None
    task_id: Optional[str] = None
    backend_used: str
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict) 