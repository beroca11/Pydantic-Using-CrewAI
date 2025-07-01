from crewai import Agent, Task
from typing import List
from models import VoiceSegment, VoiceStyle, GeneratedScript
from tools.elevenlabs_api import ElevenLabsAPI, MockElevenLabsAPI
import os


class VoiceAgent:
    """Agent responsible for generating voice narration"""
    
    def __init__(self):
        # Initialize ElevenLabs API (use mock if no API key)
        try:
            self.elevenlabs = ElevenLabsAPI()
        except ValueError:
            print("Using mock ElevenLabs API for testing")
            self.elevenlabs = MockElevenLabsAPI()
        
        # Create CrewAI agent
        self.agent = Agent(
            role="Voice Narration Specialist",
            goal="Generate high-quality voice narration that matches the script and style",
            backstory="Expert in voice synthesis and audio production",
            verbose=True,
            allow_delegation=False
        )
    
    def create_voice_task(self, script: GeneratedScript, voice_style: VoiceStyle, language: str) -> Task:
        """Create a task for voice generation"""
        return Task(
            description=f"Generate voice narration for script with {voice_style.value} style",
            agent=self.agent,
            expected_output="Voice segments with audio files and timing"
        )
    
    async def generate_voice(self, script: GeneratedScript, voice_style: VoiceStyle, language: str) -> List[VoiceSegment]:
        """Generate voice narration for script segments"""
        try:
            # Extract text from script segments
            text_segments = [segment.text for segment in script.segments]
            
            # Generate voice using ElevenLabs
            voice_segments = await self.elevenlabs.generate_voice_segments(
                text_segments=text_segments,
                voice_style=voice_style,
                language=language
            )
            
            return voice_segments
            
        except Exception as e:
            print(f"Error generating voice: {e}")
            return self._create_fallback_voice(script)
    
    def _create_fallback_voice(self, script: GeneratedScript) -> List[VoiceSegment]:
        """Create fallback voice segments"""
        voice_segments = []
        current_time = 0.0
        
        for i, segment in enumerate(script.segments):
            # Estimate duration
            word_count = len(segment.text.split())
            duration = (word_count / 150) * 60  # ~150 words per minute
            
            voice_segment = VoiceSegment(
                audio_url=f"fallback_audio_{i}.mp3",
                text=segment.text,
                start_time=current_time,
                end_time=current_time + duration,
                duration=duration
            )
            
            voice_segments.append(voice_segment)
            current_time += duration
        
        return voice_segments
    
    def cleanup_audio_files(self, voice_segments: List[VoiceSegment]):
        """Clean up temporary audio files"""
        self.elevenlabs.cleanup_temp_files(voice_segments) 