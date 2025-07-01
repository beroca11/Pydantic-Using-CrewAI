import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { 
  CheckCircle, 
  AlertCircle, 
  Loader2, 
  Download, 
  Play, 
  ArrowLeft,
  Clock,
  FileVideo,
  ExternalLink,
  Share2,
  Eye,
  Zap,
  Sparkles
} from 'lucide-react'
import { getJobStatus, getJobResult, downloadVideo } from '../services/api'
import type { JobProgress, VideoResult } from '../services/api'

export const JobStatus: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()
  const [progress, setProgress] = useState<JobProgress | null>(null)
  const [result, setResult] = useState<VideoResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isDownloading, setIsDownloading] = useState(false)

  useEffect(() => {
    if (!jobId) return

    const fetchStatus = async () => {
      try {
        const status = await getJobStatus(jobId)
        setProgress(status)

        // If completed, fetch the result
        if (status.status === 'completed') {
          const videoResult = await getJobResult(jobId)
          setResult(videoResult)
        }
      } catch (err) {
        setError('Failed to fetch job status')
        console.error(err)
      }
    }

    // Initial fetch
    fetchStatus()

    // Poll for updates if not completed
    const interval = setInterval(() => {
      if (progress?.status === 'completed' || progress?.status === 'failed') {
        clearInterval(interval)
        return
      }
      fetchStatus()
    }, 2000)

    return () => clearInterval(interval)
  }, [jobId, progress?.status])

  const handleDownload = async () => {
    if (!jobId || !result) return

    setIsDownloading(true)
    try {
      const downloadUrl = await downloadVideo(jobId)
      
      // Create download link
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = `video_${jobId}.mp4`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } catch (err) {
      console.error('Download failed:', err)
      alert('Download failed. Please try again.')
    } finally {
      setIsDownloading(false)
    }
  }

  const getStatusIcon = () => {
    if (!progress) return <Loader2 className="w-8 h-8 animate-spin text-primary-600" />

    switch (progress.status) {
      case 'completed':
        return <CheckCircle className="w-8 h-8 text-success-600" />
      case 'failed':
        return <AlertCircle className="w-8 h-8 text-danger-600" />
      case 'processing':
        return <Zap className="w-8 h-8 text-accent-600 animate-pulse" />
      default:
        return <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
    }
  }

  const getStatusColor = () => {
    if (!progress) return 'from-gray-400 to-gray-500'

    switch (progress.status) {
      case 'completed':
        return 'from-success-500 to-success-600'
      case 'failed':
        return 'from-danger-500 to-danger-600'
      case 'processing':
        return 'from-accent-500 to-accent-600'
      default:
        return 'from-primary-500 to-primary-600'
    }
  }

  const getStatusText = () => {
    if (!progress) return 'Loading...'
    
    switch (progress.status) {
      case 'completed':
        return 'Video Ready!'
      case 'failed':
        return 'Generation Failed'
      case 'processing':
        return 'Creating Magic...'
      default:
        return progress.current_step || 'Processing...'
    }
  }

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'Unknown'
    const mb = bytes / (1024 * 1024)
    return `${mb.toFixed(1)} MB`
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto animate-fade-in">
        <div className="card p-8 text-center">
          <div className="w-16 h-16 bg-danger-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <AlertCircle className="w-8 h-8 text-danger-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Oops! Something went wrong</h2>
          <p className="text-gray-600 mb-8 text-lg">{error}</p>
          <Link to="/" className="btn-primary">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Generator
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 animate-slide-up">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold gradient-text mb-2">Video Generation</h1>
          <p className="text-gray-600 text-lg">Job ID: <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">{jobId}</span></p>
        </div>
        <Link to="/" className="btn-secondary">
          <ArrowLeft className="w-5 h-5 mr-2" />
          Create Another
        </Link>
      </div>

      {/* Progress Card */}
      <div className="card p-8 mb-8 animate-slide-up" style={{animationDelay: '0.1s'}}>
        <div className="flex items-center mb-8">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-200/50 to-accent-200/50 blur-lg rounded-full"></div>
            <div className="relative bg-white rounded-full p-4 shadow-medium">
              {getStatusIcon()}
            </div>
          </div>
          <div className="ml-6 flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {getStatusText()}
            </h2>
            <p className="text-gray-600 text-lg">
              {progress?.current_step && progress.status !== 'completed' && progress.current_step}
              {progress?.status === 'completed' && 'Your amazing video is ready to download!'}
              {progress?.status === 'failed' && 'We encountered an issue during generation'}
              {!progress && 'Initializing your video generation...'}
            </p>
          </div>
          {progress?.status === 'completed' && (
            <div className="animate-float">
              <Sparkles className="w-8 h-8 text-accent-500" />
            </div>
          )}
        </div>

        {/* Progress Bar */}
        {progress && (
          <div className="mb-6">
            <div className="flex justify-between items-center mb-3">
              <span className="text-sm font-medium text-gray-700">Progress</span>
              <span className="text-sm font-bold text-primary-600">{Math.round(progress.progress)}%</span>
            </div>
            <div className="progress-bar">
              <div
                className={`progress-fill bg-gradient-to-r ${getStatusColor()}`}
                style={{ width: `${progress.progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Error Message */}
        {progress?.error_message && (
          <div className="bg-danger-50 border border-danger-200 rounded-xl p-6 mb-6 animate-scale-in">
            <div className="flex items-start">
              <AlertCircle className="w-6 h-6 text-danger-600 mr-3 mt-0.5" />
              <div>
                <h3 className="font-semibold text-danger-800 mb-1">Error Details</h3>
                <p className="text-danger-700">{progress.error_message}</p>
              </div>
            </div>
          </div>
        )}

        {/* Timestamps */}
        {progress && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div className="flex items-center text-gray-600">
              <Clock className="w-5 h-5 mr-3 text-gray-400" />
              <div>
                <div className="font-medium">Started</div>
                <div>{new Date(progress.created_at).toLocaleString()}</div>
              </div>
            </div>
            <div className="flex items-center text-gray-600">
              <Clock className="w-5 h-5 mr-3 text-gray-400" />
              <div>
                <div className="font-medium">Last Updated</div>
                <div>{new Date(progress.updated_at).toLocaleString()}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Video Result */}
      {result && (
        <div className="card p-8 animate-slide-up" style={{animationDelay: '0.2s'}}>
          <div className="flex items-center mb-8">
                         <div className="w-12 h-12 bg-gradient-to-r from-success-500 to-success-600 rounded-xl flex items-center justify-center mr-4">
              <FileVideo className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Your Video is Ready!</h2>
              <p className="text-gray-600">High-quality AI-generated video with synchronized audio</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 xl:grid-cols-5 gap-8">
            {/* Video Player */}
            <div className="xl:col-span-3">
              <div className="video-container aspect-video">
                <video
                  src={result.video_url}
                  controls
                  className="w-full h-full"
                  poster={result.thumbnail_url}
                >
                  Your browser does not support the video tag.
                </video>
              </div>
            </div>

            {/* Video Info & Actions */}
            <div className="xl:col-span-2 space-y-6">
              <div className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl border border-gray-100">
                <h3 className="font-bold text-gray-900 mb-4 text-lg">Video Details</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 flex items-center">
                      <Clock className="w-4 h-4 mr-2" />
                      Duration
                    </span>
                    <span className="font-semibold text-gray-900">{formatDuration(Math.round(result.duration))}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 flex items-center">
                      <FileVideo className="w-4 h-4 mr-2" />
                      File Size
                    </span>
                    <span className="font-semibold text-gray-900">{formatFileSize(result.file_size)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 flex items-center">
                      <Eye className="w-4 h-4 mr-2" />
                      Quality
                    </span>
                    <span className="font-semibold text-gray-900">HD 1080p</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Created</span>
                    <span className="font-semibold text-gray-900">{new Date(result.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <button
                  onClick={handleDownload}
                  disabled={isDownloading}
                  className="btn-success w-full flex items-center justify-center text-lg py-4"
                >
                  {isDownloading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-3 animate-spin" />
                      Downloading...
                    </>
                  ) : (
                    <>
                      <Download className="w-5 h-5 mr-3" />
                      Download Video
                    </>
                  )}
                </button>

                <a
                  href={result.video_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-outline w-full flex items-center justify-center text-lg py-4"
                >
                  <ExternalLink className="w-5 h-5 mr-3" />
                  Open in New Tab
                </a>

                <button className="btn-secondary w-full flex items-center justify-center text-lg py-4">
                  <Share2 className="w-5 h-5 mr-3" />
                  Share Video
                </button>
              </div>

              <div className="text-center text-sm text-gray-500 pt-4 border-t border-gray-200">
                <p>💡 Tip: Right-click the video to save or share directly</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 