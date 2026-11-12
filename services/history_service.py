
from database.db import db
from database.models import HumanizationHistory


class HistoryService:

    @staticmethod
    def save_humanization(
        client_id: str,
        original_text: str,
        result_text: str,
        model_id: str,
        prompt_id: int,
        prompt_snapshot: str,
        processing_time: float = None
    ):
        history = HumanizationHistory(
            client_id=client_id,
            original_text=original_text,
            result_text=result_text,
            model_id=model_id,
            prompt_id=prompt_id,
            prompt_snapshot=prompt_snapshot,
            processing_time=processing_time
        )

        try:
            db.session.add(history)
            db.session.commit()
            return history

        except Exception:
            db.session.rollback()
            raise
