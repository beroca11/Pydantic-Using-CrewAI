import os
import asyncio
import httpx
from typing import List, Optional
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
from models import VoiceSegment, VoiceStyle


class ElevenLabsAPI:
    """Tool for generating voice narration using ElevenLabs API"""
    
    def __init__(self):
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        
        # Initialize the new ElevenLabs client
        self.client = ElevenLabs(api_key=api_key)
        
        # Voice ID mappings for different styles
        self.voice_ids = {
            VoiceStyle.NARRATIVE: "21m00Tcm4TlvDq8ikWAM",  # Rachel - Professional
            VoiceStyle.CONVERSATIONAL: "AZnzlk1XvdvUeBnXmlld",  # Domi - Casual
            VoiceStyle.PROFESSIONAL: "EXAVITQu4vr4xnSDxMaL",  # Bella - Professional
            VoiceStyle.CASUAL: "VR6AewLTigWG4xSOukaG",  # Arnold - Casual
            VoiceStyle.DRAMATIC: "pNInz6obpgDQGcFmaJgB"  # Adam - Dramatic
        }
    
    async def generate_voice_segments(
        self, 
        text_segments: List[str], 
        voice_style: VoiceStyle = VoiceStyle.NARRATIVE,
        language: str = "en"
    ) -> List[VoiceSegment]:
        """
        Generate voice narration for text segments
        
        Args:
            text_segments: List of text segments to narrate
            voice_style: Style of voice to use
            language: Language code for voice generation
            
        Returns:
            List of VoiceSegment objects with audio URLs and timing
        """
        try:
            voice_id = self.voice_ids.get(voice_style, self.voice_ids[VoiceStyle.NARRATIVE])
            
            voice_segments = []
            current_time = 0.0
            
            for i, text in enumerate(text_segments):
                # Generate audio for this segment using new API
                audio = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )
                
                # Save audio to temporary file
                temp_filename = f"temp_voice_segment_{i}.mp3"
                save(audio, temp_filename)
                
                # Estimate duration (rough calculation: ~150 words per minute)
                word_count = len(text.split())
                duration = (word_count / 150) * 60  # seconds
                
                # Create voice segment
                segment = VoiceSegment(
                    audio_url=temp_filename,  # In production, upload to cloud storage
                    text=text,
                    start_time=current_time,
                    end_time=current_time + duration,
                    duration=duration
                )
                
                voice_segments.append(segment)
                current_time += duration
            
            return voice_segments
            
        except Exception as e:
            raise Exception(f"Failed to generate voice segments: {str(e)}")
    
    async def get_available_voices(self) -> List[dict]:
        """Get list of available voices from ElevenLabs"""
        try:
            response = self.client.voices.search()
            voices = response.voices
            return [
                {
                    "id": voice.voice_id,
                    "name": voice.name,
                    "category": getattr(voice, 'category', 'general'),
                    "description": getattr(voice, 'description', '')
                }
                for voice in voices
            ]
        except Exception as e:
            print(f"Warning: Could not fetch available voices: {e}")
            return []
    
    def cleanup_temp_files(self, voice_segments: List[VoiceSegment]):
        """Clean up temporary audio files"""
        for segment in voice_segments:
            if os.path.exists(segment.audio_url):
                try:
                    os.remove(segment.audio_url)
                except Exception as e:
                    print(f"Warning: Could not remove temp file {segment.audio_url}: {e}")


# Mock implementation for testing without API key
class MockElevenLabsAPI:
    """Mock implementation for testing without ElevenLabs API key"""
    
    async def generate_voice_segments(
        self, 
        text_segments: List[str], 
        voice_style: VoiceStyle = VoiceStyle.NARRATIVE,
        language: str = "en"
    ) -> List[VoiceSegment]:
        """Mock voice generation that returns placeholder segments"""
        import time
        
        voice_segments = []
        current_time = 0.0
        
        for i, text in enumerate(text_segments):
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            # Estimate duration
            word_count = len(text.split())
            duration = (word_count / 150) * 60
            
            segment = VoiceSegment(
                audio_url=f"mock_audio_segment_{i}.mp3",
                text=text,
                start_time=current_time,
                end_time=current_time + duration,
                duration=duration
            )
            
            voice_segments.append(segment)
            current_time += duration
        
        return voice_segments
    
    async def get_available_voices(self) -> List[dict]:
        """Return mock available voices"""
        return [
            {"id": "mock_1", "name": "Rachel", "category": "professional"},
            {"id": "mock_2", "name": "Domi", "category": "casual"},
            {"id": "mock_3", "name": "Bella", "category": "professional"}
        ]
    
    def cleanup_temp_files(self, voice_segments: List[VoiceSegment]):
        """Mock cleanup - no files to clean"""
        pass 