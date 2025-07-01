from crewai import Agent, Task
from typing import List, Dict, Any
from openai import OpenAI
import os
from models import GeneratedScript, ScriptSegment, VideoStyle, VoiceStyle


class ScriptAgent:
    """Agent responsible for generating story scripts from user prompts"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client with new v1.0.0+ format
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Create CrewAI agent
        self.agent = Agent(
            role="Creative Story Writer",
            goal="Create engaging, well-structured video scripts",
            backstory="Expert creative writer with experience in video production",
            verbose=True,
            allow_delegation=False
        )
    
    def create_script_task(self, prompt: str, style: VideoStyle, voice_style: VoiceStyle, duration: int) -> Task:
        """Create a task for script generation"""
        return Task(
            description=f"Create a compelling video script for: {prompt}",
            agent=self.agent,
            expected_output="A structured script with title, summary, and timed segments"
        )
    
    def generate_script(self, prompt: str, style: VideoStyle, voice_style: VoiceStyle, duration: int) -> GeneratedScript:
        """Generate script using OpenAI"""
        try:
            system_prompt = f"Create a {duration}-second video script in {style.value} style with {voice_style.value} narration."
            
            # Use new OpenAI v1.0.0+ format
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Create segments based on content
            segments = self._parse_script_to_segments(content, duration)
            
            return GeneratedScript(
                title=f"Story about {prompt}",
                segments=segments,
                total_duration=duration,
                summary=f"A narrative about {prompt}"
            )
            
        except Exception as e:
            print(f"Error generating script: {e}")
            return self._create_fallback_script(prompt, duration)
    
    def _parse_script_to_segments(self, content: str, duration: int) -> List[ScriptSegment]:
        """Parse script content into timed segments"""
        # Simple parsing - split by sentences
        sentences = content.split('. ')
        num_segments = min(len(sentences), 5)
        segment_duration = duration / num_segments
        
        segments = []
        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration
            
            segment = ScriptSegment(
                text=sentences[i] + ".",
                start_time=start_time,
                end_time=end_time,
                scene_description=f"Scene {i + 1}"
            )
            segments.append(segment)
        
        return segments
    
    def _create_fallback_script(self, prompt: str, duration: int) -> GeneratedScript:
        """Create a simple fallback script"""
        num_segments = 3
        segment_duration = duration / num_segments
        
        segments = []
        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration
            
            segment = ScriptSegment(
                text=f"Segment {i + 1} about {prompt}.",
                start_time=start_time,
                end_time=end_time,
                scene_description=f"Scene {i + 1}"
            )
            segments.append(segment)
        
        return GeneratedScript(
            title=f"Story about {prompt}",
            segments=segments,
            total_duration=duration,
            summary=f"A narrative about {prompt}"
        )


# Mock implementation for testing
class MockScriptAgent:
    """Mock implementation for testing without OpenAI API"""
    
    def __init__(self):
        self.agent = Agent(
            role="Mock Story Writer",
            goal="Create mock scripts for testing",
            backstory="Mock agent for testing purposes",
            verbose=True,
            allow_delegation=False
        )
    
    def create_script_task(self, prompt: str, style: VideoStyle, voice_style: VoiceStyle, duration: int) -> Task:
        return Task(
            description=f"Generate mock script for: {prompt}",
            agent=self.agent,
            expected_output="Mock script data"
        )
    
    def generate_script(self, prompt: str, style: VideoStyle, voice_style: VoiceStyle, duration: int) -> GeneratedScript:
        import asyncio
        asyncio.sleep(0.5)
        
        num_segments = 3
        segment_duration = duration / num_segments
        
        segments = []
        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration
            
            segment = ScriptSegment(
                text=f"This is segment {i + 1} about {prompt}.",
                start_time=start_time,
                end_time=end_time,
                scene_description=f"Scene {i + 1}"
            )
            segments.append(segment)
        
        return GeneratedScript(
            title=f"The Amazing World of {prompt}",
            segments=segments,
            total_duration=duration,
            summary=f"An exploration of {prompt}"
        ) 