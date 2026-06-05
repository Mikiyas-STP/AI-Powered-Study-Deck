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
            raise e

    @staticmethod
    def rephrase_flashcard(front_text:str, back_text:str) -> dict:
        """
        Sends front and back text of a flashcard to Groq AI to rephrase and improve it.
        If it fails or if the key is invalid, returns a mocked offline fallback.
        """
        prompt = f"""
        You are an expert copyeditor. Refine and polish this study flashcard.
        Fix any grammatical errors, simplify the language to be clear and easy to understand, and make it concise, but preserve the original educational intent and scope.
        Return ONLY a JSON object with "front" and "back" keys.
        
        Original Card :
        Front: {front_text}
        Back: {back_text}
        """
        try:
            if not settings.OPENAI_API_KEY or "your_groq_api_key" in settings.OPENAI_API_KEY:
                raise ValueError("Missing or invalid Groq API Key")
            response = client.chat.completions.create(
                model = "llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            
            if "front" in data and "back" in data:
                return data
            raise ValueError("Invalid JSON response structure from AI")
        except Exception as e:
            print(f"AI Rephrase Error: {e}")
            raise e

        
ai_services = AIService()