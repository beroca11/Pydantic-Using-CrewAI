#!/usr/bin/env python3
"""
Comprehensive installation script for AI Video Generator
Installs all missing packages and dependencies
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(command, description, cwd=None, check=True):
    """Run a command with proper error handling"""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, cwd=cwd, check=check, 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(command, cwd=cwd, check=check, 
                                  capture_output=True, text=True)
        
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old. Need Python 3.8+")
        return False


def upgrade_pip():
    """Upgrade pip to latest version"""
    return run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      "Upgrading pip")


def install_core_packages():
    """Install core packages one by one"""
    print("\n📦 Installing Core Packages...")
    
    core_packages = [
        "wheel",
        "setuptools",
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-dotenv==1.0.0",
        "pydantic==2.5.0",
        "httpx==0.25.2",
        "python-multipart==0.0.6"
    ]
    
    success = True
    for package in core_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}"):
            success = False
    
    return success


def install_crewai():
    """Install CrewAI and its dependencies"""
    print("\n🤖 Installing CrewAI...")
    
    # Install CrewAI which will pull in compatible OpenAI version
    return run_command([sys.executable, "-m", "pip", "install", "crewai==0.28.0"], 
                      "Installing CrewAI")


def install_ai_packages():
    """Install AI service packages"""
    print("\n🧠 Installing AI Service Packages...")
    
    ai_packages = [
        "elevenlabs==0.2.26",
        "anthropic==0.7.8"
    ]
    
    success = True
    for package in ai_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}", check=False):
            print(f"⚠️  {package} installation failed (optional)")
    
    return success


def install_video_packages():
    """Install video processing packages"""
    print("\n🎬 Installing Video Processing Packages...")
    
    video_packages = [
        "Pillow==10.1.0",
        "moviepy==1.0.3",
        "ffmpeg-python==0.2.0"
    ]
    
    for package in video_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}", check=False):
            print(f"⚠️  {package} installation failed (optional)")
    
    return True


def install_storage_packages():
    """Install storage packages"""
    print("\n☁️  Installing Storage Packages...")
    
    storage_packages = [
        "supabase==2.0.2",
        "boto3==1.34.0"
    ]
    
    for package in storage_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}", check=False):
            print(f"⚠️  {package} installation failed (optional)")
    
    return True


def install_background_packages():
    """Install background task packages"""
    print("\n⚙️  Installing Background Task Packages...")
    
    bg_packages = [
        "celery==5.3.4",
        "redis==5.0.1"
    ]
    
    for package in bg_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}", check=False):
            print(f"⚠️  {package} installation failed (optional)")
    
    return True


def install_dev_packages():
    """Install development packages"""
    print("\n🛠️  Installing Development Packages...")
    
    dev_packages = [
        "pytest==7.4.3",
        "black==23.11.0",
        "isort==5.12.0"
    ]
    
    for package in dev_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}", check=False):
            print(f"⚠️  {package} installation failed (optional)")
    
    return True


def check_node_and_npm():
    """Check if Node.js and npm are installed"""
    print("\n🟢 Checking Node.js and npm...")
    
    try:
        # Check Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        print("📥 Please install Node.js from: https://nodejs.org/")
        return False
    
    try:
        # Check npm
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False


def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("\n🌐 Installing Frontend Dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    if not run_command(["npm", "install"], "Installing npm packages", cwd=frontend_dir):
        return False
    
    print("✅ Frontend dependencies installed")
    return True


def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up Environment...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    # Create .env file
    env_content = """# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
POLLO_API_KEY=your_pollo_api_key_here

# Storage Configuration (Optional)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# AWS S3 (Alternative to Supabase)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_S3_BUCKET=your_s3_bucket_name_here
AWS_REGION=us-east-1

# Redis for background tasks
REDIS_URL=redis://localhost:6379

# App Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def install_ffmpeg():
    """Provide instructions for FFmpeg installation"""
    print("\n🎥 FFmpeg Installation...")
    
    system = platform.system().lower()
    
    if system == "windows":
        print("📥 To install FFmpeg on Windows:")
        print("   1. Download from: https://ffmpeg.org/download.html")
        print("   2. Extract to C:\\ffmpeg")
        print("   3. Add C:\\ffmpeg\\bin to your PATH")
        print("   4. Or use chocolatey: choco install ffmpeg")
    elif system == "darwin":  # macOS
        print("📥 To install FFmpeg on macOS:")
        print("   brew install ffmpeg")
        try:
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
            print("✅ FFmpeg installed via Homebrew")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Homebrew not found or FFmpeg installation failed")
    elif system == "linux":
        print("📥 To install FFmpeg on Linux:")
        print("   Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
        print("   CentOS/RHEL: sudo yum install ffmpeg")
        print("   Arch: sudo pacman -S ffmpeg")
    
    return True


def main():
    """Main installation function"""
    print("🎬 AI Video Generator - Quick Fix Installation")
    print("=" * 60)
    
    # Upgrade pip first
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
               "Upgrading pip")
    
    # Install core packages
    if not install_core_packages():
        print("❌ Core package installation failed")
        return
    
    # Install CrewAI
    if not install_crewai():
        print("❌ CrewAI installation failed")
        return
    
    # Install frontend dependencies
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        install_frontend_dependencies()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Node.js not found. Please install Node.js from https://nodejs.org/")
    
    print("\n✅ Installation completed!")
    print("🚀 Run: python test_installation.py to verify")


if __name__ == "__main__":
    main() 