import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

export interface VideoOptions {
  resolution: string
  length: number
  generateAudio: boolean
  quality: string
}

export interface VideoRequest {
  prompt: string
  style: string
  voiceStyle: string
  duration: number
  language: string
  backend?: string
  videoOptions?: VideoOptions
}

export interface JobResponse {
  job_id: string
  status: string
  message?: string
  estimated_time?: string
}

export interface JobProgress {
  job_id: string
  status: string
  progress: number
  current_step: string
  estimated_completion?: string
  error_message?: string
  created_at: string
  updated_at: string
  backend?: string
}

export interface VideoResult {
  job_id: string
  video_url: string
  thumbnail_url?: string
  duration: number
  file_size?: number
  metadata: Record<string, any>
  created_at: string
  backend_used?: string
}

export const generateVideo = async (request: VideoRequest): Promise<JobResponse> => {
  const response = await api.post('/api/generate', {
    prompt: request.prompt,
    style: request.style,
    voice_style: request.voiceStyle,
    duration: request.duration,
    language: request.language,
    backend: request.backend || 'auto',
    video_options: request.videoOptions || {
      resolution: '1080p',
      length: 7,
      generateAudio: true,
      quality: 'high'
    }
  })
  return response.data
}

export const getJobStatus = async (jobId: string): Promise<JobProgress> => {
  const response = await api.get(`/api/job/${jobId}`)
  return response.data
}

export const getJobResult = async (jobId: string): Promise<VideoResult> => {
  const response = await api.get(`/api/job/${jobId}/result`)
  return response.data
}

export const listBackends = async (): Promise<any> => {
  const response = await api.get('/api/backends')
  return response.data
}

export const listModels = async (): Promise<any> => {
  const response = await api.get('/api/models')
  return response.data
}

export const testBackend = async (backend: string, prompt?: string): Promise<any> => {
  const response = await api.post('/api/test-backend', {
    backend,
    prompt: prompt || 'A beautiful sunset over the ocean'
  })
  return response.data
}

export const listJobs = async (): Promise<Record<string, JobProgress>> => {
  const response = await api.get('/api/jobs')
  return response.data
}

export const deleteJob = async (jobId: string): Promise<void> => {
  await api.delete(`/api/jobs/${jobId}`)
}

export const downloadVideo = async (jobId: string): Promise<string> => {
  const response = await api.get(`/api/download/${jobId}`)
  if (response.data.video_url) {
    return response.data.video_url
  }
  // If it's a direct file download, return the blob URL
  return URL.createObjectURL(new Blob([response.data]))
} 