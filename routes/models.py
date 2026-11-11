
from flask import Blueprint, jsonify

from services.model_service import ModelService


models_bp = Blueprint("models", __name__)


def serialize_model(model):
    """Convert an AI model object to a dictionary."""
    return {
        "id": model.id,
        "name": model.name,
        "model_id": model.model_id,
        "description": model.description,
        "provider": model.provider,
        "is_active": model.is_active
    }


@models_bp.route("/models", methods=["GET"])
def get_models():
    """Return all active AI models."""

    models = ModelService.get_active_models()

    return jsonify({
        "status": "success",
        "count": len(models),
        "models": [
            serialize_model(model)
            for model in models
        ]
    }), 200


@models_bp.route("/models/<int:model_id>", methods=["GET"])
def get_model(model_id):
    """Return a specific AI model by database ID."""

    model = ModelService.get_model_by_id(model_id)

    if not model or not model.is_active:
        return jsonify({
            "status": "error",
            "message": "AI model not found"
        }), 404

    return jsonify({
        "status": "success",
        "model": serialize_model(model)
    }), 200
