from app import app

from database.db import db
from database.models import AIModel

from services.humanization_service import HumanizationService
from services.model_service import ModelService
from services.prompt_service import PromptService


class FakeHuggingFaceService:
    """Fake service for testing without real API requests."""

    def __init__(self):
        self.last_request = None

    def generate_text(self, model_id, prompt, max_tokens=500):
        self.last_request = {
            "model_id": model_id,
            "prompt": prompt,
            "max_tokens": max_tokens
        }

        return "This is a humanized test result."


def test_humanization_service():
    with app.app_context():

        client_id = "test_humanization_client"

        # Отримуємо тестову AI-модель
        models = ModelService.get_active_models()
        assert models, "No active AI models found"

        model = models[0]

        # Отримуємо стандартний промпт
        prompts = PromptService.get_default_prompts()
        assert prompts, "No default prompts found"

        prompt = prompts[0]

        fake_hf = FakeHuggingFaceService()
        service = HumanizationService(hf_service=fake_hf)

        # 1. Успішна хуманізація
        result = service.humanize(
            text="This is my original text.",
            model_id=model.id,
            prompt_id=prompt.id,
            client_id=client_id
        )

        assert result["original_text"] == "This is my original text."
        assert result["result_text"] == "This is a humanized test result."
        assert result["model_id"] == model.model_id
        assert result["prompt_id"] == prompt.id
        assert result["processing_time"] >= 0

        print("Successful humanization: OK")

        # 2. Перевірка формування запиту
        request = fake_hf.last_request

        assert prompt.content in request["prompt"]
        assert "This is my original text." in request["prompt"]
        assert request["model_id"] == model.model_id
        assert request["max_tokens"] == 500

        print("Prompt and model integration: OK")

        # 3. Перевірка власного промпту
        custom_prompt = PromptService.create_prompt(
            client_id=client_id,
            name="Test Custom Prompt",
            content="Rewrite the text in a friendly style.",
            category="general"
        )

        custom_result = service.humanize(
            text="Custom prompt test.",
            model_id=model.id,
            prompt_id=custom_prompt.id,
            client_id=client_id
        )

        assert custom_result["prompt_id"] == custom_prompt.id
        assert "friendly style" in fake_hf.last_request["prompt"]

        print("Custom prompt integration: OK")

        # 4. Перевірка порожнього тексту
        try:
            service.humanize(
                text="   ",
                model_id=model.id,
                prompt_id=prompt.id,
                client_id=client_id
            )
            assert False, "Empty text should raise ValueError"
        except ValueError:
            print("Empty text validation: OK")

        # 5. Перевірка неіснуючої моделі
        try:
            service.humanize(
                text="Test text",
                model_id=999999,
                prompt_id=prompt.id,
                client_id=client_id
            )
            assert False, "Invalid model should raise LookupError"
        except LookupError:
            print("Invalid model validation: OK")

        # 6. Перевірка неіснуючого промпту
        try:
            service.humanize(
                text="Test text",
                model_id=model.id,
                prompt_id=999999,
                client_id=client_id
            )
            assert False, "Invalid prompt should raise LookupError"
        except LookupError:
            print("Invalid prompt validation: OK")

        # 7. Перевірка доступу до чужого промпту
        try:
            service.humanize(
                text="Test text",
                model_id=model.id,
                prompt_id=custom_prompt.id,
                client_id="another_client"
            )
            assert False, "Foreign prompt should raise LookupError"
        except LookupError:
            print("Custom prompt ownership: OK")

        # 8. Перевірка порожнього результату AI
        class EmptyResponseService:
            def generate_text(self, model_id, prompt, max_tokens=500):
                return ""

        empty_service = HumanizationService(
            hf_service=EmptyResponseService()
        )

        try:
            empty_service.humanize(
                text="Test text",
                model_id=model.id,
                prompt_id=prompt.id,
                client_id=client_id
            )
            assert False, "Empty AI result should raise ValueError"
        except ValueError:
            print("Empty AI response validation: OK")

        # 9. Очищення тестових даних
        PromptService.delete_prompt(
            custom_prompt.id,
            client_id
        )

        print("Test data cleanup: OK")


if __name__ == "__main__":
    test_humanization_service()