# AI Video Generator

A full-stack application that generates realistic, narrated videos from text prompts using CrewAI, multiple AI services, and modern web technologies.

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd ai-video-generator

# 2. Run the automated setup
python setup.py

# 3. Edit .env with your API keys
# 4. Start the application
python start.py
```

Open http://localhost:3000 and start creating videos! 🎬

## 🚀 Features

- **AI-Powered Script Generation**: Uses GPT-4/Claude to create engaging video scripts
- **Voice Synthesis**: ElevenLabs integration for high-quality voice narration
- **Video Generation**: Pollo.ai Veo 3 for creating stunning video content
- **Professional Editing**: FFmpeg-powered video editing and audio synchronization
- **Cloud Storage**: Supabase/AWS S3 integration for video hosting
- **Real-time Progress**: WebSocket-like polling for live generation updates
- **Modern UI**: React + Tailwind CSS with mobile-first design

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **CrewAI Framework**: Orchestrates AI agents for modular video generation
- **Script Agent**: Generates story scripts from user prompts
- **Voice Agent**: Creates voice narration using ElevenLabs
- **Video Agent**: Generates video segments using Pollo.ai Veo 3
- **Editor Agent**: Merges audio and video using FFmpeg
- **Uploader Agent**: Handles cloud storage uploads

### Frontend (React + TypeScript)
- **Modern React**: Hooks, TypeScript, and functional components
- **Tailwind CSS**: Utility-first styling with custom design system
- **Real-time Updates**: Progress tracking and status polling
- **Responsive Design**: Mobile-first, accessible interface

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- FFmpeg (optional, for video processing)
- API Keys for:
  - OpenAI (GPT-4)
  - ElevenLabs
  - Pollo.ai
  - Supabase or AWS S3 (optional)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-video-generator
   ```

2. **Install Python dependencies**
   ```bash
   # Option 1: Use the setup script (recommended)
   python setup.py
   
   # Option 2: Use flexible requirements
   pip install -r requirements-flexible.txt
   
   # Option 3: Use fixed requirements (may have conflicts)
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # The setup script creates .env automatically
   # Or manually copy from example:
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the backend**
   ```bash
   # Development mode
   python backend/api.py
   
   # Or with uvicorn
   uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
POLLO_API_KEY=your_pollo_api_key_here

# Storage Configuration (Optional)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# AWS S3 (Alternative to Supabase)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_S3_BUCKET=your_s3_bucket_name_here

# App Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Mock Mode

The application includes mock implementations for testing without API keys:
- **Mock Script Agent**: Generates placeholder scripts
- **Mock ElevenLabs**: Returns mock audio segments
- **Mock Pollo.ai**: Returns placeholder video URLs
- **Mock FFmpeg**: Creates mock video files

## 🎯 Usage

1. **Open the application** in your browser
2. **Enter a video prompt** describing what you want to create
3. **Configure settings**:
   - Video style (Cinematic, Documentary, etc.)
   - Voice style (Narrative, Professional, etc.)
   - Duration (10-120 seconds)
   - Language preference
4. **Click "Generate Video"** to start the process
5. **Monitor progress** on the status page
6. **Download or view** your completed video

### Example Prompts

- "A peaceful sunset over the ocean with gentle waves"
- "A bustling city street at night with neon lights"
- "A serene forest path with sunlight filtering through trees"
- "A cozy coffee shop on a rainy day"

## 🛠️ Development

### Project Structure

```
project/
├── agents/                 # CrewAI agents
│   ├── script_agent.py    # Script generation
│   ├── voice_agent.py     # Voice synthesis
│   ├── video_agent.py     # Video generation
│   ├── editor_agent.py    # Video editing
│   └── uploader_agent.py  # Cloud upload
├── tools/                 # API integrations
│   ├── elevenlabs_api.py  # ElevenLabs integration
│   ├── pollo_veo3_api.py  # Pollo.ai integration
│   └── ffmpeg_utils.py    # Video processing
├── backend/               # FastAPI backend
│   └── api.py            # REST API endpoints
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   └── App.tsx       # Main app component
│   └── package.json
├── models.py              # Pydantic models
├── main.py               # CrewAI orchestrator
└── requirements.txt      # Python dependencies
```

### API Endpoints

- `POST /generate` - Start video generation
- `GET /status/{job_id}` - Get job status
- `GET /result/{job_id}` - Get video result
- `GET /jobs` - List all jobs
- `DELETE /jobs/{job_id}` - Delete job
- `GET /download/{job_id}` - Download video

### Testing

```bash
# Test the main workflow
python main.py

# Run backend tests
pytest

# Run frontend tests
cd frontend && npm test
```

## 🚀 Deployment

### Docker Deployment (Recommended)

1. **Build containers**
   ```bash
   docker-compose build
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

### Manual Deployment

1. **Backend**: Deploy to services like Railway, Render, or AWS
2. **Frontend**: Deploy to Vercel, Netlify, or AWS S3
3. **Storage**: Configure Supabase or AWS S3 for video storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **CrewAI** for the agent framework
- **ElevenLabs** for voice synthesis
- **Pollo.ai** for video generation
- **OpenAI** for script generation
- **FastAPI** and **React** for the web framework

## 🔗 Links

- [CrewAI Documentation](https://docs.crewai.com/)
- [ElevenLabs API](https://elevenlabs.io/docs)
- [Pollo.ai Documentation](https://pollo.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Built with ❤️ using modern AI and web technologies** 