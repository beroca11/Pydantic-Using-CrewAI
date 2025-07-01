#!/usr/bin/env python3
"""
Test script to verify AI Video Generator installation
"""

import sys
import importlib
from pathlib import Path


def test_import(module_name, optional=False):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        if optional:
            print(f"⚠️  {module_name} (optional) - {e}")
        else:
            print(f"❌ {module_name} - {e}")
        return not optional


def test_installation():
    """Test the complete installation"""
    print("🧪 Testing AI Video Generator Installation")
    print("=" * 50)
    
    # Test core dependencies
    print("\n📦 Core Dependencies:")
    core_success = True
    core_modules = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "httpx",
        "dotenv"
    ]
    
    for module in core_modules:
        if not test_import(module):
            core_success = False
    
    # Test CrewAI
    print("\n🤖 CrewAI Framework:")
    crewai_success = test_import("crewai")
    
    # Test AI dependencies
    print("\n🧠 AI Dependencies:")
    ai_success = True
    ai_modules = [
        ("openai", False),
        ("elevenlabs", True),
        ("anthropic", True)
    ]
    
    for module, optional in ai_modules:
        if not test_import(module, optional):
            if not optional:
                ai_success = False
    
    # Test video processing
    print("\n🎬 Video Processing:")
    video_modules = [
        ("moviepy", True),
        ("PIL", True),  # Pillow
        ("ffmpeg", True)
    ]
    
    for module, optional in video_modules:
        test_import(module, optional)
    
    # Test storage
    print("\n☁️  Storage (Optional):")
    storage_modules = [
        ("supabase", True),
        ("boto3", True)
    ]
    
    for module, optional in storage_modules:
        test_import(module, optional)
    
    # Test files
    print("\n📁 Configuration Files:")
    required_files = [
        "models.py",
        "main.py", 
        "backend/api.py",
        "start.py"
    ]
    
    files_success = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            files_success = False
    
    # Check .env
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env")
    else:
        print("⚠️  .env (run setup.py to create)")
    
    # Frontend check
    print("\n🌐 Frontend:")
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        print("✅ frontend directory")
        
        package_json = frontend_dir / "package.json"
        if package_json.exists():
            print("✅ package.json")
        else:
            print("❌ package.json")
        
        node_modules = frontend_dir / "node_modules"
        if node_modules.exists():
            print("✅ node_modules")
        else:
            print("⚠️  node_modules (run: cd frontend && npm install)")
    else:
        print("❌ frontend directory")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Installation Summary:")
    
    if core_success and crewai_success and ai_success and files_success:
        print("✅ Installation looks good!")
        print("🚀 You can run: python start.py")
        return True
    else:
        print("❌ Installation has issues")
        print("🔧 Try running: python setup.py")
        return False


if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1) 