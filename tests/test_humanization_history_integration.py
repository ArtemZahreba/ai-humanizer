
from unittest.mock import patch

from app import app
from services.humanization_service import HumanizationService
from services.model_service import ModelService
from services.prompt_service import PromptService


class FakeHuggingFaceService:
    def generate_text(self, model_id, prompt, max_tokens=500):
        return "Humanized test result."


def test_humanization_saves_history():
    with app.app_context():
        client_id = "test_history_integration"

        models = ModelService.get_active_models()
        prompts = PromptService.get_default_prompts()

        assert models, "No active AI models found"
        assert prompts, "No default prompts found"

        model = models[0]
        prompt = prompts[0]

        service = HumanizationService(
            hf_service=FakeHuggingFaceService()
        )

        with patch(
            "services.humanization_service.HistoryService.save_humanization"
        ) as history_mock:

            result = service.humanize(
                text="Original test text.",
                model_id=model.id,
                prompt_id=prompt.id,
                client_id=client_id
            )

            history_mock.assert_called_once()

            saved_data = history_mock.call_args.kwargs

            assert saved_data["client_id"] == client_id
            assert saved_data["original_text"] == "Original test text."
            assert saved_data["result_text"] == "Humanized test result."
            assert saved_data["model_id"] == model.model_id
            assert saved_data["prompt_id"] == prompt.id
            assert saved_data["prompt_snapshot"] == prompt.content
            assert saved_data["processing_time"] >= 0

        assert result["result_text"] == "Humanized test result."

        print("SUCCESS: Humanization history integration test passed!")


if __name__ == "__main__":
    test_humanization_saves_history()
    print("\nAll integration tests passed!")
