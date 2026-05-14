# app/services/ai_service.py
import json
from typing import List, Dict
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIService:
    @staticmethod
    def generate_flashcards(text_content: str) -> List[Dict[str, str]]:
        """
        Sends text to OpenAI and asks for a list of Flashcards in JSON format.
        """
        prompt = f"""
        You are an expert educator. Convert the following text into a list of concise flashcards.
        Each flashcard must have a 'front' (question/concept) and a 'back' (answer/definition).
        Return ONLY a JSON array of objects.
        
        Text: {text_content}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125", # Or gpt-4o-mini
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} # Ensures valid JSON
        )

        # Parse the response
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # We expect the AI to return {"flashcards": [{"front": "...", "back": "..."}, ...]}
        return data.get("flashcards", [])

ai_service = AIService()