# app/services/ai_service.py (MOCK VERSION)
import time

class AIService:
    @staticmethod
    def generate_flashcards(text_content: str):
        """
        A fake AI service that doesn't need a key.
        Use this to test your database and React frontend first!
        """
        print(f"DEBUG: Mocking AI generation for text: {text_content[:20]}...")
        
        # Simulate a 1-second delay so it feels like AI
        time.sleep(1) 
        
        return [
            {
                "front": "What is the capital of France?",
                "back": "Paris"
            },
            {
                "front": "What does PAPR stand for?",
                "back": "PostgreSQL, API (FastAPI), Python, React"
            }
        ]

ai_service = AIService()