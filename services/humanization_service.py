import time

from services.huggingface_service import HuggingFaceService
from services.model_service import ModelService
from services.prompt_service import PromptService


class HumanizationService:
    """Service responsible for text humanization."""

    def __init__(self, hf_service=None):
        # Дозволяє підмінити Hugging Face сервіс під час тестування
        self.hf_service = hf_service or HuggingFaceService()

    def humanize(
        self,
        text: str,
        model_id: int,
        prompt_id: int,
        client_id: str,
        max_tokens: int = 500
    ):
        """Humanize text using the selected AI model and prompt."""

        # 1. Перевіряємо вхідні дані
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text is required")

        if not isinstance(client_id, str) or not client_id.strip():
            raise ValueError("Client ID is required")

        if not isinstance(max_tokens, int) or isinstance(max_tokens, bool) or max_tokens <= 0:
            raise ValueError("Max tokens must be a positive integer")

        # 2. Отримуємо AI-модель
        model = ModelService.get_model_by_id(model_id)

        if not model or not model.is_active:
            raise LookupError("AI model not found or inactive")

        # 3. Отримуємо промпт
        prompt = PromptService.get_prompt_by_id(
            prompt_id=prompt_id,
            client_id=client_id
        )

        if not prompt:
            raise LookupError("Prompt not found")

        # 4. Формуємо фінальний запит
        final_prompt = (
            f"{prompt.content}\n\n"
            f"Text to humanize:\n{text.strip()}"
        )

        # 5. Відправляємо запит до Hugging Face
        start_time = time.perf_counter()

        result = self.hf_service.generate_text(
            model_id=model.model_id,
            prompt=final_prompt,
            max_tokens=max_tokens
        )

        processing_time = time.perf_counter() - start_time

        if not isinstance(result, str) or not result.strip():
            raise ValueError("AI returned an empty result")

        # 6. Повертаємо результат
        return {
            "original_text": text.strip(),
            "result_text": result.strip(),
            "model_id": model.model_id,
            "prompt_id": prompt.id,
            "processing_time": round(processing_time, 3)
        }