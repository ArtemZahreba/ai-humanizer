
from uuid import uuid4

from app import app
from database.db import db
from database.models import HumanizationHistory
from services.history_service import HistoryService


def test_get_history_by_id():
    with app.app_context():
        client_id = f"test_{uuid4().hex}"
        another_client_id = f"test_{uuid4().hex}"

        record = HumanizationHistory(
            client_id=client_id,
            original_text="Original text",
            result_text="Humanized text",
            model_id="deepseek-ai/DeepSeek-R1:novita",
            prompt_id=None,
            prompt_snapshot="Rewrite naturally.",
            processing_time=1.25
        )

        db.session.add(record)
        db.session.commit()

        try:
            # 1. Успішне отримання запису
            history = HistoryService.get_history_by_id(
                history_id=record.id,
                client_id=client_id
            )

            assert history is not None
            assert history["id"] == record.id
            assert history["original_text"] == "Original text"
            assert history["result_text"] == "Humanized text"
            assert history["model_id"] == "deepseek-ai/DeepSeek-R1:novita"
            assert history["prompt_snapshot"] == "Rewrite naturally."
            assert history["processing_time"] == 1.25

            print("SUCCESS: Get history by ID test passed!")

            # 2. Перевірка неіснуючого запису
            missing_history = HistoryService.get_history_by_id(
                history_id=999999999,
                client_id=client_id
            )

            assert missing_history is None

            print("SUCCESS: Missing history test passed!")

            # 3. Перевірка доступу іншого клієнта
            foreign_history = HistoryService.get_history_by_id(
                history_id=record.id,
                client_id=another_client_id
            )

            assert foreign_history is None

            print("SUCCESS: Foreign history access test passed!")

            # 4. Перевірка некоректного client_id
            try:
                HistoryService.get_history_by_id(
                    history_id=record.id,
                    client_id=" "
                )
                assert False, "Invalid client ID should raise ValueError"
            except ValueError:
                print("SUCCESS: Invalid client ID test passed!")

            # 5. Перевірка некоректного history_id
            try:
                HistoryService.get_history_by_id(
                    history_id="invalid",
                    client_id=client_id
                )
                assert False, "Invalid history ID should raise ValueError"
            except ValueError:
                print("SUCCESS: Invalid history ID test passed!")

        finally:
            db.session.rollback()

            HumanizationHistory.query.filter_by(
                id=record.id
            ).delete()

            db.session.commit()


if __name__ == "__main__":
    test_get_history_by_id()
    print("\nAll History Detail Service tests passed!")
