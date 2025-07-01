#!/usr/bin/env python3
"""
Demo script for the modular VideoAgent system
Demonstrates dynamic backend selection between Pollo.ai and ImagineArt APIs
"""

import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv

from agents.video_agent import VideoAgent
from models import (
    VideoStyle, VideoBackend, VideoGenerationOptions, 
    VideoResolution, GeneratedScript, ScriptSegment
)

# Load environment variables
load_dotenv()

async def demo_single_video_generation():
    """Demo: Generate a single video with different backends"""
    print("=" * 60)
    print("🎬 DEMO: Single Video Generation with Backend Selection")
    print("=" * 60)
    
    # Initialize the video agent
    agent = VideoAgent()
    
    # Display available backends
    backends = agent.get_available_backends()
    print(f"📱 Available backends: {', '.join(backends)}")
    
    # Test prompt
    prompt = "A majestic eagle soaring over snow-capped mountains at sunset"
    
    # Test different backends
    test_cases = [
        ("auto", "Automatic backend selection"),
        ("pollo", "Pollo.ai Veo 3 backend"),
        ("imagineart", "ImagineArt backend")
    ]
    
    for backend_name, description in test_cases:
        print(f"\n🔄 Testing {description}...")
        
        try:
            # Configure generation options
            options = {
                "resolution": "1080p",
                "length": 5,
                "generateAudio": True,
                "quality": "high"
            }
            
            # Generate video
            result = await agent.act(
                prompt=prompt,
                model_name=backend_name,
                options=options
            )
            
            if result.success:
                print(f"✅ Success! Video generated using {result.backend_used}")
                print(f"   Video URL: {result.video_url}")
                print(f"   Metadata: {result.metadata}")
            else:
                print(f"❌ Failed: {result.error_message}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def demo_script_based_generation():
    """Demo: Generate video segments from a script"""
    print("\n" + "=" * 60)
    print("📝 DEMO: Script-Based Video Generation")
    print("=" * 60)
    
    # Initialize the video agent
    agent = VideoAgent()
    
    # Create a sample script
    script = GeneratedScript(
        title="Nature Documentary: Mountain Wildlife",
        total_duration=15.0,
        summary="A short documentary about mountain wildlife",
        segments=[
            ScriptSegment(
                text="High in the mountains, where the air is thin and the views are spectacular...",
                start_time=0.0,
                end_time=5.0,
                scene_description="Panoramic view of snow-capped mountain peaks with morning mist"
            ),
            ScriptSegment(
                text="Wildlife has adapted to survive in these harsh conditions.",
                start_time=5.0,
                end_time=10.0,
                scene_description="Mountain goats gracefully navigating rocky cliffs"
            ),
            ScriptSegment(
                text="Each creature plays a vital role in this alpine ecosystem.",
                start_time=10.0,
                end_time=15.0,
                scene_description="Golden eagle circling above the peaks, hunting for prey"
            )
        ]
    )
    
    # Test with different styles and backends
    test_combinations = [
        (VideoStyle.DOCUMENTARY, VideoBackend.AUTO, "Documentary style with auto backend"),
        (VideoStyle.CINEMATIC, VideoBackend.POLLO, "Cinematic style with Pollo.ai"),
        (VideoStyle.ARTISTIC, VideoBackend.IMAGINEART, "Artistic style with ImagineArt")
    ]
    
    for style, backend, description in test_combinations:
        print(f"\n🎨 Testing {description}...")
        
        try:
            # Configure video options
            options = VideoGenerationOptions(
                resolution=VideoResolution.FULL_HD_1080P,
                length=5,
                generateAudio=False,  # No audio for segments
                quality="high"
            )
            
            # Generate video segments
            segments = await agent.generate_videos(
                script=script,
                style=style,
                backend=backend,
                options=options
            )
            
            print(f"✅ Generated {len(segments)} video segments:")
            for i, segment in enumerate(segments):
                print(f"   Segment {i+1}: {segment.video_url}")
                print(f"   Backend: {segment.backend_used}")
                print(f"   Duration: {segment.duration}s")
                print(f"   Scene: {segment.scene_description[:50]}...")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def demo_backend_comparison():
    """Demo: Compare performance and results across backends"""
    print("\n" + "=" * 60)
    print("⚡ DEMO: Backend Performance Comparison")
    print("=" * 60)
    
    agent = VideoAgent()
    
    # Test prompt that works well with both backends
    prompt = "A serene lake reflecting autumn trees with gentle ripples"
    
    # Test different resolutions and settings
    test_configs = [
        {
            "name": "Quick Test (720p, 3s)",
            "options": {"resolution": "720p", "length": 3, "quality": "standard"}
        },
        {
            "name": "Standard Quality (1080p, 5s)", 
            "options": {"resolution": "1080p", "length": 5, "quality": "high"}
        },
        {
            "name": "Long Form (1080p, 8s)",
            "options": {"resolution": "1080p", "length": 8, "quality": "high"}
        }
    ]
    
    backends = ["pollo", "imagineart"]
    
    for config in test_configs:
        print(f"\n📊 Testing: {config['name']}")
        print("-" * 40)
        
        for backend in backends:
            try:
                import time
                start_time = time.time()
                
                result = await agent.act(
                    prompt=prompt,
                    model_name=backend,
                    options=config["options"]
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                if result.success:
                    print(f"✅ {backend.upper()}: {duration:.1f}s - {result.video_url}")
                else:
                    print(f"❌ {backend.upper()}: Failed - {result.error_message}")
                    
            except Exception as e:
                print(f"❌ {backend.upper()}: Error - {str(e)}")

async def demo_available_models():
    """Demo: List available models from all backends"""
    print("\n" + "=" * 60)
    print("🔍 DEMO: Available Models and Capabilities")
    print("=" * 60)
    
    agent = VideoAgent()
    
    try:
        models = await agent.list_available_models()
        
        for backend, model_list in models.items():
            print(f"\n🤖 {backend.upper()} Models:")
            if model_list:
                for model in model_list:
                    print(f"   • {model.get('name', 'Unknown')}")
                    print(f"     ID: {model.get('id', 'N/A')}")
                    print(f"     Description: {model.get('description', 'No description')}")
            else:
                print("   No models available or API not accessible")
                
    except Exception as e:
        print(f"❌ Error fetching models: {str(e)}")

async def demo_fallback_logic():
    """Demo: Test fallback logic when primary backend fails"""
    print("\n" + "=" * 60)
    print("🔄 DEMO: Fallback Logic Testing")
    print("=" * 60)
    
    agent = VideoAgent()
    
    # Simulate a scenario where we prefer one backend but it might fail
    prompt = "A futuristic city with flying cars and neon lights"
    
    print("🔧 Testing fallback behavior...")
    print("   1. Try auto mode (should attempt Pollo first, then ImagineArt)")
    
    try:
        result = await agent.act(
            prompt=prompt,
            model_name="auto",
            options={"resolution": "1080p", "length": 6}
        )
        
        print(f"   Result: {'✅ Success' if result.success else '❌ Failed'}")
        print(f"   Backend used: {result.backend_used}")
        
        if result.success:
            print(f"   Video URL: {result.video_url}")
        else:
            print(f"   Error: {result.error_message}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")

async def main():
    """Run all demonstrations"""
    print("🚀 Starting VideoAgent Multi-Backend Demo")
    print("This demo will test the modular video generation system")
    
    # Check environment setup
    print("\n🔧 Environment Check:")
    pollo_key = "✅" if os.getenv("POLLO_API_KEY") else "❌ (using mock)"
    imagineart_key = "✅" if os.getenv("IMAGINEART_API_KEY") else "❌ (using mock)"
    print(f"   Pollo.ai API Key: {pollo_key}")
    print(f"   ImagineArt API Key: {imagineart_key}")
    
    # Run demonstrations
    try:
        await demo_single_video_generation()
        await demo_script_based_generation()
        await demo_backend_comparison() 
        await demo_available_models()
        await demo_fallback_logic()
        
        print("\n" + "=" * 60)
        print("✅ All demos completed successfully!")
        print("🎬 Your VideoAgent system is ready for production use.")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main()) 