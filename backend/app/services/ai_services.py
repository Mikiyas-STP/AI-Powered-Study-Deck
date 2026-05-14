# app/services/ai_service.py
import time
from typing import List, Dict

class AIService:
    @staticmethod
    def generate_flashcards(text_content: str) -> List[Dict[str, str]]:
        """
        MOCK SERVICE: Simulates AI processing.
        In a real scenario, this would call OpenAI/Groq.
        """
        # Simulate network latency (1.5 seconds)
        time.sleep(1.5)
        
        # We'll return some dynamic-ish content based on the input length
        # just to make it feel a bit more real.
        return [
            {
                "front": f"Key Concept from your notes",
                "back": f"Detailed explanation of the text: {text_content[:30]}..."
            },
            {
                "front": "PAPR Stack Definition",
                "back": "PostgreSQL, API (FastAPI), Python, React."
            },
            {
                "front": "Spaced Repetition",
                "back": "A learning technique that performs reviews at increasing intervals."
            }
        ]

ai_service = AIService()