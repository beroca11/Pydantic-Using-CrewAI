#!/usr/bin/env python3
"""
Startup script for AI Video Generator
Runs both backend and frontend development servers
"""

import subprocess
import sys
import os
import time
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    try:
        import fastapi
        import uvicorn
        import crewai
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check if frontend dependencies are installed
    frontend_dir = Path("frontend")
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    else:
        print("✅ Frontend dependencies found")
    
    return True


def check_environment():
    """Check environment configuration"""
    print("🔧 Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("📝 Creating .env from example...")
        
        env_example = Path("env.example")
        if env_example.exists():
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created from example")
            print("🚨 Please edit .env with your API keys before running")
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ .env file found")
    
    return True


def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    
    try:
        # Start uvicorn server
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.api:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        print("✅ Backend server starting on http://localhost:8000")
        return backend_process
    
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None


def start_frontend():
    """Start the React frontend server"""
    print("🚀 Starting frontend server...")
    
    try:
        frontend_dir = Path("frontend")
        frontend_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=frontend_dir)
        
        print("✅ Frontend server starting on http://localhost:3000")
        return frontend_process
    
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None


def main():
    """Main startup function"""
    print("🎬 AI Video Generator - Startup Script")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed")
        sys.exit(1)
    
    print("\n🚀 Starting servers...")
    print("=" * 50)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        sys.exit(1)
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n✅ Both servers started successfully!")
    print("=" * 50)
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    print("\n🛑 Press Ctrl+C to stop both servers")
    
    try:
        # Wait for user to stop
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        print("✅ Servers stopped")
        sys.exit(0)


if __name__ == "__main__":
    main() 