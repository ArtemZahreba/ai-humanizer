
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app import app
from database.db import db
from database.models import HumanizationHistory
from services.history_service import HistoryService


def test_get_history():
    with app.app_context():
        client_id = f"test_{uuid4().hex}"
        another_client_id = f"test_{uuid4().hex}"

        now = datetime.now(timezone.utc)

        first_record = HumanizationHistory(
            client_id=client_id,
            original_text="First original text",
            result_text="First result",
            model_id="test/model",
            prompt_snapshot="Test prompt",
            processing_time=1.2,
            created_at=now
        )

        second_record = HumanizationHistory(
            client_id=client_id,
            original_text="Second original text",
            result_text="Second result",
            model_id="test/model",
            prompt_snapshot="Test prompt",
            processing_time=2.5,
            created_at=now + timedelta(seconds=1)
        )

        foreign_record = HumanizationHistory(
            client_id=another_client_id,
            original_text="Foreign text",
            result_text="Foreign result",
            model_id="test/model",
            prompt_snapshot="Test prompt",
            processing_time=1.0
        )

        try:
            db.session.add_all([
                first_record,
                second_record,
                foreign_record
            ])
            db.session.commit()

            history = HistoryService.get_history(client_id)

            # Перевіряємо кількість записів
            assert len(history) == 2

            # Перевіряємо сортування: новіші записи першими
            assert history[0]["original_text"] == "Second original text"
            assert history[1]["original_text"] == "First original text"

            # Перевіряємо структуру відповіді
            assert history[0]["result_text"] == "Second result"
            assert history[0]["model_id"] == "test/model"
            assert history[0]["processing_time"] == 2.5
            assert history[0]["created_at"] is not None

            # Перевіряємо, що чужий запис не потрапив в історію
            assert all(
                record["original_text"] != "Foreign text"
                for record in history
            )

            print("SUCCESS: Get history test passed!")

        finally:
            db.session.rollback()

            HumanizationHistory.query.filter(
                HumanizationHistory.client_id.in_([
                    client_id,
                    another_client_id
                ])
            ).delete(synchronize_session=False)

            db.session.commit()


def test_get_history_invalid_client_id():
    with app.app_context():
        try:
            HistoryService.get_history("   ")
            assert False, "Invalid client ID should raise ValueError"
        except ValueError:
            print("SUCCESS: Invalid client ID test passed!")


if __name__ == "__main__":
    test_get_history()
    test_get_history_invalid_client_id()

    print("\nAll GetHistoryService tests passed!")
