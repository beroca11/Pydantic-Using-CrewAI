#!/usr/bin/env python3
"""
Simplified test script for the modular VideoAgent system
Demonstrates the multi-backend architecture and features
"""

import asyncio
import os
from typing import Dict, Any, Optional

# Mock classes to demonstrate the system without full dependencies
class MockVideoAgent:
    """Mock VideoAgent to demonstrate the multi-backend functionality"""
    
    def __init__(self):
        # Simulate checking for API keys
        self.pollo_available = bool(os.getenv("POLLO_API_KEY"))
        self.imagineart_available = bool(os.getenv("IMAGINEART_API_KEY"))
        
        # Determine available backends
        self.available_backends = []
        if self.pollo_available:
            self.available_backends.append("pollo")
        if self.imagineart_available:
            self.available_backends.append("imagineart")
        
        # If no real APIs, use mock backends
        if not self.available_backends:
            self.available_backends = ["pollo", "imagineart"]
            print("🔧 Using mock APIs (no API keys found)")
        else:
            print(f"✅ Real APIs available: {', '.join(self.available_backends)}")
    
    def get_available_backends(self):
        """Get list of available backends"""
        return self.available_backends
    
    async def act(self, prompt: str, model_name: str = "auto", options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Mock video generation with backend selection"""
        if options is None:
            options = {}
        
        print(f"🎬 Generating video with backend: {model_name}")
        print(f"   Prompt: {prompt[:50]}...")
        print(f"   Options: {options}")
        
        # Simulate processing time
        await asyncio.sleep(1.0)
        
        # Mock backend selection logic
        if model_name == "auto":
            chosen_backend = "pollo" if "pollo" in self.available_backends else "imagineart"
            print(f"   🔄 Auto-selected backend: {chosen_backend}")
        else:
            chosen_backend = model_name
        
        # Mock successful generation
        video_id = hash(prompt) % 10000
        
        if chosen_backend == "pollo":
            video_url = f"https://mock-pollo-storage.com/video_{video_id}.mp4"
        else:
            video_url = f"https://mock-imagineart-storage.com/video_{video_id}.mp4"
        
        return {
            "success": True,
            "video_url": video_url,
            "backend_used": chosen_backend,
            "metadata": {
                "resolution": options.get("resolution", "1080p"),
                "length": options.get("length", 7),
                "quality": options.get("quality", "high")
            }
        }
    
    async def list_available_models(self) -> Dict[str, Any]:
        """Mock available models listing"""
        return {
            "pollo": [
                {"id": "veo-3", "name": "Veo 3", "description": "Latest video generation model"}
            ] if "pollo" in self.available_backends else [],
            "imagineart": [
                {"id": "text-to-video-v2", "name": "Text to Video v2", "description": "Latest model"}
            ] if "imagineart" in self.available_backends else []
        }

async def demo_basic_functionality():
    """Demo basic video generation functionality"""
    print("=" * 60)
    print("🎬 DEMO: Basic Video Generation")
    print("=" * 60)
    
    agent = MockVideoAgent()
    
    print(f"📱 Available backends: {', '.join(agent.get_available_backends())}")
    
    # Test prompt
    prompt = "A majestic eagle soaring over snow-capped mountains at sunset"
    
    # Test different backends
    backends = ["auto", "pollo", "imagineart"]
    
    for backend in backends:
        print(f"\n🔄 Testing {backend} backend...")
        
        try:
            result = await agent.act(
                prompt=prompt,
                model_name=backend,
                options={
                    "resolution": "1080p",
                    "length": 5,
                    "generateAudio": True,
                    "quality": "high"
                }
            )
            
            if result["success"]:
                print(f"   ✅ Success! Backend: {result['backend_used']}")
                print(f"   📹 Video URL: {result['video_url']}")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")

async def demo_backend_features():
    """Demo advanced backend features"""
    print("\n" + "=" * 60)
    print("🔧 DEMO: Backend Features")
    print("=" * 60)
    
    agent = MockVideoAgent()
    
    # Show available models
    print("🔍 Available models:")
    models = await agent.list_available_models()
    
    for backend, model_list in models.items():
        print(f"   {backend.upper()}:")
        if model_list:
            for model in model_list:
                print(f"      • {model['name']} ({model['id']})")
                print(f"        {model['description']}")
        else:
            print("      No models available")
    
    # Test different configurations
    print(f"\n⚙️  Testing different configurations:")
    
    test_configs = [
        {"name": "High Quality 4K", "options": {"resolution": "4k", "quality": "high", "length": 8}},
        {"name": "Quick HD", "options": {"resolution": "720p", "quality": "standard", "length": 3}},
        {"name": "Standard Full HD", "options": {"resolution": "1080p", "quality": "high", "length": 5}}
    ]
    
    for config in test_configs:
        print(f"\n   📊 {config['name']}:")
        result = await agent.act(
            prompt="A serene lake at sunset",
            model_name="auto",
            options=config["options"]
        )
        print(f"      Backend: {result['backend_used']}")
        print(f"      Metadata: {result['metadata']}")

def show_architecture_info():
    """Show information about the system architecture"""
    print("\n" + "=" * 60)
    print("🏗️  SYSTEM ARCHITECTURE")
    print("=" * 60)
    
    print("""
📦 Modular VideoAgent Architecture:

🎯 Core Components:
   • VideoAgent - Multi-backend orchestrator with fallback logic
   • PolloVeo3API - High-quality cinematic video generation
   • ImagineArtAPI - Fast, multi-style video generation
   • MockAPIs - Testing and development without API keys

🔄 Backend Selection:
   • AUTO mode: Tries Pollo.ai first, falls back to ImagineArt
   • MANUAL mode: User selects specific backend
   • FALLBACK logic: Automatic retry with alternative backend

⚙️  Configuration Options:
   • Resolution: 720p, 1080p, 4K
   • Quality: Standard, High
   • Length: 3-10 seconds per segment
   • Audio: Enable/disable audio generation

🌐 API Integration:
   • Environment variables for API keys
   • Async/await for non-blocking operations
   • Comprehensive error handling
   • Real-time progress tracking

🎬 Usage Examples:
   • Single video generation with prompt
   • Script-based multi-segment videos
   • Bulk generation with different styles
   • Performance comparison between backends
""")

def show_usage_examples():
    """Show usage examples for the system"""
    print("\n" + "=" * 60)
    print("💡 USAGE EXAMPLES")
    print("=" * 60)
    
    print("""
🐍 Python Code Examples:

1️⃣ Basic Video Generation:
```python
from agents.video_agent import VideoAgent

agent = VideoAgent()
result = await agent.act(
    prompt="A peaceful sunset over the ocean",
    model_name="auto",
    options={"resolution": "1080p", "length": 5}
)
```

2️⃣ Specific Backend Selection:
```python
# Use Pollo.ai specifically
result = await agent.act(
    prompt="Cinematic mountain landscape",
    model_name="pollo",
    options={"resolution": "4k", "quality": "high"}
)
```

3️⃣ Frontend Integration:
```typescript
const response = await generateVideo({
  prompt: "A futuristic city at night",
  style: "cinematic",
  backend: "auto",
  videoOptions: {
    resolution: "1080p",
    length: 7,
    generateAudio: true,
    quality: "high"
  }
})
```

4️⃣ Environment Setup:
```bash
# .env file
POLLO_API_KEY=your_pollo_api_key_here
IMAGINEART_API_KEY=your_imagineart_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

5️⃣ Running the System:
```bash
# Run comprehensive demo
python main.py demo

# Run quick test
python main.py test

# Start web server
python main.py server
```
""")

async def main():
    """Main demo function"""
    print("🚀 Pydantic AI VideoAgent - Multi-Backend Demo")
    print("Enhanced modular video generation system")
    
    # Check environment
    print(f"\n🔧 Environment Check:")
    pollo_key = "✅" if os.getenv("POLLO_API_KEY") else "❌ (using mock)"
    imagineart_key = "✅" if os.getenv("IMAGINEART_API_KEY") else "❌ (using mock)"
    print(f"   Pollo.ai API Key: {pollo_key}")
    print(f"   ImagineArt API Key: {imagineart_key}")
    
    try:
        # Run demonstrations
        await demo_basic_functionality()
        await demo_backend_features()
        
        # Show system information
        show_architecture_info()
        show_usage_examples()
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("🎬 Your modular VideoAgent system is ready!")
        print("=" * 60)
        
        print(f"\n📋 Next Steps:")
        print(f"   1. Add your API keys to .env file")
        print(f"   2. Run 'python main.py server' to start the web interface")
        print(f"   3. Open http://localhost:3000 in your browser")
        print(f"   4. Create stunning AI videos with multi-backend support!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main()) 