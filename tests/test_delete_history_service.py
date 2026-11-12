
from uuid import uuid4

from app import app
from database.db import db
from database.models import HumanizationHistory
from services.history_service import HistoryService


def test_delete_history():
    with app.app_context():
        client_id = f"test_{uuid4().hex}"

        record = HumanizationHistory(
            client_id=client_id,
            original_text="Original text",
            result_text="Humanized text",
            model_id="test/model",
            prompt_snapshot="Test prompt",
            processing_time=1.2
        )

        db.session.add(record)
        db.session.commit()

        history_id = record.id

        # 1. Успішне видалення
        result = HistoryService.delete_history(
            history_id=history_id,
            client_id=client_id
        )

        assert result is True
        assert db.session.get(HumanizationHistory, history_id) is None

        print("SUCCESS: Delete history test passed!")

        # 2. Видалення неіснуючого запису
        result = HistoryService.delete_history(
            history_id=999999999,
            client_id=client_id
        )

        assert result is False

        print("SUCCESS: Missing history deletion test passed!")

        # 3. Перевірка некоректного client_id
        try:
            HistoryService.delete_history(
                history_id=history_id,
                client_id=" "
            )
            assert False, "Invalid client ID should raise ValueError"
        except ValueError:
            print("SUCCESS: Invalid client ID test passed!")

        # 4. Перевірка некоректного history_id
        try:
            HistoryService.delete_history(
                history_id="invalid",
                client_id=client_id
            )
            assert False, "Invalid history ID should raise ValueError"
        except ValueError:
            print("SUCCESS: Invalid history ID test passed!")


if __name__ == "__main__":
    test_delete_history()
    print("\nAll Delete History Service tests passed!")
