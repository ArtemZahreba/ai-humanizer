
from app import app
from database.db import db
from database.models import Prompt, HumanizationHistory
from services.history_service import HistoryService


def test_save_humanization():
    with app.app_context():
        prompt = Prompt(
            name="Test Prompt",
            description="Test description",
            content="Rewrite the text naturally.",
            category="test",
            is_default=True
        )

        db.session.add(prompt)
        db.session.commit()

        history = HistoryService.save_humanization(
            client_id="test_client",
            original_text="Original text",
            result_text="Humanized text",
            model_id="deepseek-ai/DeepSeek-R1:novita",
            prompt_id=prompt.id,
            prompt_snapshot=prompt.content,
            processing_time=1.25
        )

        saved_history = db.session.get(
            HumanizationHistory,
            history.id
        )

        assert saved_history is not None
        assert saved_history.client_id == "test_client"
        assert saved_history.original_text == "Original text"
        assert saved_history.result_text == "Humanized text"
        assert saved_history.model_id == "deepseek-ai/DeepSeek-R1:novita"
        assert saved_history.prompt_id == prompt.id
        assert saved_history.prompt_snapshot == prompt.content
        assert saved_history.processing_time == 1.25

        print("SUCCESS: Save humanization test passed!")

        db.session.delete(saved_history)
        db.session.delete(prompt)
        db.session.commit()


def test_save_humanization_without_processing_time():
    with app.app_context():
        prompt = Prompt(
            name="Test Prompt",
            content="Rewrite naturally.",
            category="test",
            is_default=True
        )

        db.session.add(prompt)
        db.session.commit()

        history = HistoryService.save_humanization(
            client_id="test_client",
            original_text="Original",
            result_text="Result",
            model_id="test/model",
            prompt_id=prompt.id,
            prompt_snapshot=prompt.content
        )

        assert history.processing_time is None

        db.session.delete(history)
        db.session.delete(prompt)
        db.session.commit()

        print("SUCCESS: Optional processing time test passed!")


def run_tests():
    test_save_humanization()
    test_save_humanization_without_processing_time()

    print("\nAll HistoryService tests passed!")


if __name__ == "__main__":
    run_tests()
