
from flask import Blueprint, jsonify

from services.model_service import ModelService


models_bp = Blueprint("models", __name__)


@models_bp.route("/models", methods=["GET"])
def get_models():
    """Return all active AI models."""

    models = ModelService.get_active_models()

    return jsonify({
        "status": "success",
        "count": len(models),
        "models": [
            {
                "id": model.id,
                "name": model.name,
                "model_id": model.model_id,
                "description": model.description,
                "provider": model.provider
            }
            for model in models
        ]
    }), 200
