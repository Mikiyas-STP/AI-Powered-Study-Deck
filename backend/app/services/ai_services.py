# app/services/ai_services.py
import json
from openai import OpenAI
from app.core.config import settings

# Groq is OpenAI-compatible, we just change the base_url
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

class AIService:
    @staticmethod
    def generate_flashcards(text_content: str):
        """
        Sends text to Groq AI and returns structured flashcards.
        """
        prompt = f"""
        Extract the most important educational concepts from the text below.
        Return a JSON object with a key "flashcards" containing a list of objects.
        Each object must have "front" (the question) and "back" (the answer).
        
        Text: {text_content}
        """

        # We use Llama 3 - it's incredibly fast and smart
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("flashcards", [])

ai_services = AIService()