from database.db import db
from database.models import AIModel

class ModelService:
    """Service for managing AI models."""

    @staticmethod
    def get_all_models():
        """Return all AI models."""
        return AIModel.query.order_by(AIModel.id).all()

    @staticmethod
    def get_active_models():
        """Return only active AI models."""
        return AIModel.query.filter_by(
            is_active=True
        ).order_by(AIModel.id).all()

    @staticmethod
    def get_model_by_id(model_id: int):
        """Find an AI model by its database ID."""
        return db.session.get(AIModel, model_id)

    @staticmethod
    def get_model_by_model_id(model_id: str):
        """Find an AI model by its Hugging Face model ID."""
        return AIModel.query.filter_by(
            model_id=model_id
        ).first()
