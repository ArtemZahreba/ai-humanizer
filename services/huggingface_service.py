
from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    APIStatusError,
)

from config import Config


class HuggingFaceServiceError(Exception):
    """Base exception for Hugging Face service errors."""

    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


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
        try:
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

        except RateLimitError as error:
            raise HuggingFaceServiceError(
                "AI service rate limit exceeded. Please try again later.",
                429
            ) from error

        except NotFoundError as error:
            raise HuggingFaceServiceError(
                "Selected AI model is currently unavailable.",
                503
            ) from error

        except (AuthenticationError, PermissionDeniedError) as error:
            raise HuggingFaceServiceError(
                "AI service authentication failed. Please contact support.",
                502
            ) from error

        except (APIConnectionError, APITimeoutError) as error:
            raise HuggingFaceServiceError(
                "Unable to connect to AI service. Please try again.",
                503
            ) from error

        except APIStatusError as error:
            raise HuggingFaceServiceError(
                "AI service encountered an error. Please try again later.",
                502
            ) from error
