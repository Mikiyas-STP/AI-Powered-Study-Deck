import json
from openai import OpenAI
from app.core.config import settings

# Groq is OpenAI-compatible. We just point the 'base_url' to Groq's servers.
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

class AIService:
    @staticmethod
    def generate_flashcards(text_content: str):
        """
        Sends text to Groq AI (Llama 3) and returns structured JSON flashcards.
        """
        prompt = f"""
        You are an expert teacher. Create a list of flashcards from the text below.
        Return ONLY a JSON object with a key "flashcards".
        Each flashcard must have "front" and "back" keys.
        
        Text: {text_content}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # One of the fastest models on Groq
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            # Parse the string response into a Python dictionary
            content = response.choices[0].message.content
            data = json.loads(content)
            return data.get("flashcards", [])
        except Exception as e:
            print(f"AI Error: {e}")
            return []

ai_services = AIService()