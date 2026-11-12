
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


    @staticmethod
    def get_history(client_id: str):
        if not isinstance(client_id, str) or not client_id.strip():
            raise ValueError("Client ID is required")

        history_records = (
            HumanizationHistory.query
            .filter_by(client_id=client_id)
            .order_by(HumanizationHistory.created_at.desc())
            .all()
        )

        return [
            {
                "id": record.id,
                "original_text": record.original_text,
                "result_text": record.result_text,
                "model_id": record.model_id,
                "prompt_id": record.prompt_id,
                "processing_time": record.processing_time,
                "created_at": (
                    record.created_at.isoformat()
                    if record.created_at else None
                )
            }
            for record in history_records
        ]


    @staticmethod
    def get_history_by_id(history_id: int, client_id: str):
        if not isinstance(client_id, str) or not client_id.strip():
            raise ValueError("Client ID is required")

        if not isinstance(history_id, int) or isinstance(history_id, bool):
            raise ValueError("Valid history ID is required")

        record = HumanizationHistory.query.filter_by(
            id=history_id,
            client_id=client_id
        ).first()

        if not record:
            return None

        return {
            "id": record.id,
            "original_text": record.original_text,
            "result_text": record.result_text,
            "model_id": record.model_id,
            "prompt_id": record.prompt_id,
            "prompt_snapshot": record.prompt_snapshot,
            "processing_time": record.processing_time,
            "created_at": (
                record.created_at.isoformat()
                if record.created_at else None
            )
        }


    @staticmethod
    def delete_history(history_id: int, client_id: str):
        if not isinstance(client_id, str) or not client_id.strip():
            raise ValueError("Client ID is required")

        if not isinstance(history_id, int) or isinstance(history_id, bool):
            raise ValueError("Valid history ID is required")

        record = HumanizationHistory.query.filter_by(
            id=history_id,
            client_id=client_id
        ).first()

        if not record:
            return False

        try:
            db.session.delete(record)
            db.session.commit()
            return True

        except Exception:
            db.session.rollback()
            raise

