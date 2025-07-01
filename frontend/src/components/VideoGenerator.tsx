import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Play, 
  Loader2, 
  Settings, 
  Sparkles, 
  Wand2, 
  Film, 
  Clock, 
  Mic, 
  Globe,
  ChevronDown,
  ChevronUp,
  Rocket,
  Palette,
  Volume2,
  Camera,
  Eye,
  Brush,
  Cpu,
  Zap,
  Shield
} from 'lucide-react'
import { generateVideo } from '../services/api'

interface VideoForm {
  prompt: string
  style: string
  voiceStyle: string
  duration: number
  language: string
  backend: string
  videoOptions: {
    resolution: string
    length: number
    generateAudio: boolean
    quality: string
  }
}

const videoStyles = [
  { value: 'cinematic', label: 'Cinematic', icon: Film, description: 'Hollywood-style dramatic visuals' },
  { value: 'documentary', label: 'Documentary', icon: Camera, description: 'Realistic and informative style' },
  { value: 'animated', label: 'Animated', icon: Palette, description: 'Cartoon and animated graphics' },
  { value: 'realistic', label: 'Realistic', icon: Eye, description: 'Photorealistic imagery' },
  { value: 'artistic', label: 'Artistic', icon: Brush, description: 'Creative and stylized visuals' },
]

const voiceStyles = [
  { value: 'narrative', label: 'Narrative', description: 'Storytelling voice' },
  { value: 'conversational', label: 'Conversational', description: 'Casual and friendly' },
  { value: 'professional', label: 'Professional', description: 'Business presentation style' },
  { value: 'casual', label: 'Casual', description: 'Relaxed and informal' },
  { value: 'dramatic', label: 'Dramatic', description: 'Intense and compelling' },
]

const videoBackends = [
  { 
    value: 'auto', 
    label: 'Auto', 
    icon: Cpu, 
    description: 'Best quality with automatic fallback',
    recommended: true
  },
  { 
    value: 'pollo', 
    label: 'Pollo.ai', 
    icon: Zap, 
    description: 'High quality cinematic videos'
  },
  { 
    value: 'imagineart', 
    label: 'ImagineArt', 
    icon: Shield, 
    description: 'Fast generation, multiple styles'
  },
]

export const VideoGenerator: React.FC = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState<VideoForm>({
    prompt: '',
    style: 'cinematic',
    voiceStyle: 'narrative',
    duration: 30,
    language: 'en',
    backend: 'auto',
    videoOptions: {
      resolution: '1080p',
      length: 7,
      generateAudio: true,
      quality: 'high'
    }
  })
  const [isGenerating, setIsGenerating] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.prompt.trim()) return

    setIsGenerating(true)
    try {
      const response = await generateVideo({
        prompt: form.prompt,
        style: form.style,
        voiceStyle: form.voiceStyle,
        duration: form.duration,
        language: form.language,
        backend: form.backend,
        videoOptions: form.videoOptions
      })
      navigate(`/job/${response.job_id}`)
    } catch (error) {
      console.error('Failed to start video generation:', error)
      alert('Failed to start video generation. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleInputChange = (field: keyof VideoForm, value: string | number | object) => {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  const handleVideoOptionChange = (option: string, value: string | number | boolean) => {
    setForm(prev => ({
      ...prev,
      videoOptions: {
        ...prev.videoOptions,
        [option]: value
      }
    }))
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="relative mb-8">
          <div className="absolute inset-0 bg-gradient-to-r from-sunset-800/10 to-amber-700/10 blur-3xl -z-10 animate-pulse-slow"></div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-100 mb-6 leading-tight">
            Create Stunning 
            <span className="block gradient-text">AI Videos</span>
          </h1>
          <div className="section-divider"></div>
        </div>
        
        <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
          Transform your ideas into professional narrated videos using cutting-edge AI technology
        </p>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 max-w-2xl mx-auto">
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text">30s</div>
            <div className="text-sm text-gray-400">Average Generation</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text">4K</div>
            <div className="text-sm text-gray-400">Quality Output</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text">AI</div>
            <div className="text-sm text-gray-400">Multi-Backend</div>
          </div>
        </div>
      </div>

      {/* Main Form */}
      <div className="card p-8 mb-12 animate-slide-up">
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Prompt Input */}
          <div>
            <label htmlFor="prompt" className="block text-lg font-semibold text-gray-200 mb-3">
              <div className="flex items-center space-x-2">
                <Wand2 className="w-5 h-5 text-sunset-400" />
                <span>Describe Your Video</span>
                <span className="text-sunset-400">*</span>
              </div>
            </label>
            <div className="relative">
              <textarea
                id="prompt"
                value={form.prompt}
                onChange={(e) => handleInputChange('prompt', e.target.value)}
                placeholder="Example: A serene mountain landscape at sunrise with golden light reflecting off a pristine lake..."
                className="input-field h-40 resize-none text-lg"
                required
              />
              <div className="absolute bottom-4 right-4 text-sm text-gray-500">
                {form.prompt.length}/500
              </div>
            </div>
            <p className="text-sm text-gray-400 mt-3 flex items-center">
              <Sparkles className="w-4 h-4 mr-1 text-sunset-400" />
              Be specific and descriptive for best results
            </p>
          </div>

          {/* Backend Selection */}
          <div>
            <label className="block text-lg font-semibold text-gray-200 mb-4">
              <div className="flex items-center space-x-2">
                <Cpu className="w-5 h-5 text-sunset-400" />
                <span>AI Backend</span>
                <span className="text-xs bg-sunset-500/20 text-sunset-300 px-2 py-1 rounded-full">NEW</span>
              </div>
            </label>
            <div className="grid grid-cols-1 gap-3">
              {videoBackends.map((backend) => (
                <label
                  key={backend.value}
                  className={`relative flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                    form.backend === backend.value
                      ? 'border-sunset-600/60 bg-sunset-900/20 shadow-glow-subtle'
                      : 'border-dark-700/50 hover:border-sunset-700/40 bg-dark-700/20 hover:bg-dark-600/30'
                  }`}
                >
                  <input
                    type="radio"
                    name="backend"
                    value={backend.value}
                    checked={form.backend === backend.value}
                    onChange={(e) => handleInputChange('backend', e.target.value)}
                    className="sr-only"
                  />
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center mr-4 ${
                    form.backend === backend.value 
                      ? 'bg-button-gradient text-white' 
                      : 'bg-dark-600/50 text-gray-400'
                  }`}>
                    <backend.icon className="w-5 h-5" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium text-gray-200">{backend.label}</span>
                      {backend.recommended && (
                        <span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded-full">
                          Recommended
                        </span>
                      )}
                    </div>
                    <div className="text-sm text-gray-400">{backend.description}</div>
                  </div>
                  {form.backend === backend.value && (
                    <div className="absolute top-2 right-2">
                      <div className="w-3 h-3 bg-sunset-500 rounded-full"></div>
                    </div>
                  )}
                </label>
              ))}
            </div>
            <p className="text-sm text-gray-400 mt-3 flex items-center">
              <Shield className="w-4 h-4 mr-1 text-sunset-400" />
              Auto mode tries the best quality backend first with automatic fallback
            </p>
          </div>

          {/* Style Selection */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <label className="block text-lg font-semibold text-gray-200 mb-4">
                <div className="flex items-center space-x-2">
                  <Palette className="w-5 h-5 text-sunset-400" />
                  <span>Video Style</span>
                </div>
              </label>
              <div className="grid grid-cols-1 gap-3">
                {videoStyles.map((style) => (
                  <label
                    key={style.value}
                    className={`relative flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 ${
                      form.style === style.value
                        ? 'border-sunset-600/60 bg-sunset-900/20 shadow-glow-subtle'
                        : 'border-dark-700/50 hover:border-sunset-700/40 bg-dark-700/20 hover:bg-dark-600/30'
                    }`}
                  >
                    <input
                      type="radio"
                      name="style"
                      value={style.value}
                      checked={form.style === style.value}
                      onChange={(e) => handleInputChange('style', e.target.value)}
                      className="sr-only"
                    />
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center mr-4 ${
                      form.style === style.value 
                        ? 'bg-button-gradient text-white' 
                        : 'bg-dark-600/50 text-gray-400'
                    }`}>
                      <style.icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-200">{style.label}</div>
                      <div className="text-sm text-gray-400">{style.description}</div>
                    </div>
                    {form.style === style.value && (
                      <div className="absolute top-2 right-2">
                        <div className="w-3 h-3 bg-sunset-500 rounded-full"></div>
                      </div>
                    )}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-lg font-semibold text-gray-200 mb-4">
                <div className="flex items-center space-x-2">
                  <Clock className="w-5 h-5 text-sunset-400" />
                  <span>Duration</span>
                </div>
              </label>
              <div className="bg-dark-700/30 backdrop-blur-sm rounded-xl p-6 border border-dark-700/40">
                <input
                  type="range"
                  id="duration"
                  min="10"
                  max="120"
                  step="5"
                  value={form.duration}
                  onChange={(e) => handleInputChange('duration', parseInt(e.target.value))}
                  className="w-full mb-4"
                />
                <div className="flex justify-between text-sm text-gray-400 mb-4">
                  <span>10s</span>
                  <span className="font-bold text-2xl text-sunset-400">{form.duration}s</span>
                  <span>120s</span>
                </div>
                <div className="text-center text-sm text-gray-400">
                  Recommended: 30-60 seconds for optimal engagement
                </div>
              </div>
            </div>
          </div>

          {/* Advanced Settings Toggle */}
          <div className="border-t border-dark-700/30 pt-6">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="flex items-center justify-between w-full p-4 bg-dark-700/20 hover:bg-dark-600/30 rounded-xl transition-colors duration-300 border border-dark-700/30"
            >
              <div className="flex items-center space-x-2 text-gray-300 font-medium">
                <Settings className="w-5 h-5 text-sunset-400" />
                <span>Advanced Settings</span>
              </div>
              {showAdvanced ? (
                <ChevronUp className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-400" />
              )}
            </button>
          </div>

          {/* Advanced Settings */}
          {showAdvanced && (
            <div className="border border-dark-700/40 rounded-xl p-6 bg-dark-700/20 backdrop-blur-sm animate-slide-up">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="block text-lg font-semibold text-gray-200 mb-4">
                    <div className="flex items-center space-x-2">
                      <Volume2 className="w-5 h-5 text-sunset-400" />
                      <span>Voice Style</span>
                    </div>
                  </label>
                  <div className="space-y-3">
                    {voiceStyles.map((voice) => (
                      <label
                        key={voice.value}
                        className={`flex items-center p-3 rounded-lg border cursor-pointer transition-all duration-300 ${
                          form.voiceStyle === voice.value
                            ? 'border-sunset-600/50 bg-sunset-900/20'
                            : 'border-dark-700/50 hover:border-sunset-700/30 bg-dark-700/20 hover:bg-dark-600/30'
                        }`}
                      >
                        <input
                          type="radio"
                          name="voiceStyle"
                          value={voice.value}
                          checked={form.voiceStyle === voice.value}
                          onChange={(e) => handleInputChange('voiceStyle', e.target.value)}
                          className="sr-only"
                        />
                        <div className="flex-1">
                          <div className="font-medium text-gray-200">{voice.label}</div>
                          <div className="text-sm text-gray-400">{voice.description}</div>
                        </div>
                        {form.voiceStyle === voice.value && (
                          <div className="w-2 h-2 bg-sunset-500 rounded-full"></div>
                        )}
                      </label>
                    ))}
                  </div>
                </div>

                <div className="space-y-6">
                  <div>
                    <label htmlFor="language" className="block text-lg font-semibold text-gray-200 mb-4">
                      <div className="flex items-center space-x-2">
                        <Globe className="w-5 h-5 text-sunset-400" />
                        <span>Language</span>
                      </div>
                    </label>
                    <select
                      id="language"
                      value={form.language}
                      onChange={(e) => handleInputChange('language', e.target.value)}
                      className="input-field text-lg"
                    >
                      <option value="en">🇺🇸 English</option>
                      <option value="es">🇪🇸 Spanish</option>
                      <option value="fr">🇫🇷 French</option>
                      <option value="de">🇩🇪 German</option>
                      <option value="it">🇮🇹 Italian</option>
                      <option value="pt">🇵🇹 Portuguese</option>
                    </select>
                  </div>

                  {/* Video Options */}
                  <div>
                    <h4 className="text-lg font-semibold text-gray-200 mb-3">Video Options</h4>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">Resolution</label>
                        <select
                          value={form.videoOptions.resolution}
                          onChange={(e) => handleVideoOptionChange('resolution', e.target.value)}
                          className="input-field"
                        >
                          <option value="720p">720p (HD)</option>
                          <option value="1080p">1080p (Full HD)</option>
                          <option value="4k">4K (Ultra HD)</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">Quality</label>
                        <select
                          value={form.videoOptions.quality}
                          onChange={(e) => handleVideoOptionChange('quality', e.target.value)}
                          className="input-field"
                        >
                          <option value="standard">Standard</option>
                          <option value="high">High</option>
                        </select>
                      </div>

                      <div className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          id="generateAudio"
                          checked={form.videoOptions.generateAudio}
                          onChange={(e) => handleVideoOptionChange('generateAudio', e.target.checked)}
                          className="w-4 h-4 text-sunset-600 bg-dark-600 border-dark-500 rounded focus:ring-sunset-500"
                        />
                        <label htmlFor="generateAudio" className="text-sm font-medium text-gray-300">
                          Generate audio for video segments
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Submit Button */}
          <div className="flex justify-center pt-8">
            <button
              type="submit"
              disabled={!form.prompt.trim() || isGenerating}
              className="btn-primary flex items-center space-x-3 px-12 py-4 text-xl disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  <span>Creating Your Video...</span>
                </>
              ) : (
                <>
                  <Rocket className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
                  <span>Generate Video</span>
                  <Sparkles className="w-5 h-5 animate-pulse text-amber-200" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Features Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 animate-slide-up" style={{animationDelay: '0.2s'}}>
        <div className="feature-card group">
          <div className="feature-icon mb-6">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-gray-200 mb-3">Multi-Backend AI</h3>
          <p className="text-gray-400 leading-relaxed">
            Leverage multiple AI backends with automatic fallback for the highest success rate and quality
          </p>
        </div>

        <div className="feature-card group" style={{animationDelay: '0.1s'}}>
          <div className="feature-icon mb-6">
            <Film className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-gray-200 mb-3">Professional Quality</h3>
          <p className="text-gray-400 leading-relaxed">
            Generate 4K videos with synchronized audio, smooth transitions, and professional editing
          </p>
        </div>

        <div className="feature-card group" style={{animationDelay: '0.2s'}}>
          <div className="feature-icon mb-6">
            <Settings className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-gray-200 mb-3">Fully Customizable</h3>
          <p className="text-gray-400 leading-relaxed">
            Choose from multiple backends, styles, voices, languages, and quality settings to match your vision
          </p>
        </div>
      </div>
    </div>
  )
} 