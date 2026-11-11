
from openai import OpenAI

from config import Config


class HuggingFaceService:
    """Service for interacting with Hugging Face Inference API."""

    def __init__(self):
        if not Config.HF_TOKEN:
            raise ValueError("Hugging Face token is not configured")

        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=Config.HF_TOKEN
        )

    def generate_text(
        self,
        model_id: str,
        prompt: str,
        max_tokens: int = 500
    ) -> str:
        completion = self.client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content or ""
