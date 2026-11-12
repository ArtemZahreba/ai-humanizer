
from flask import Blueprint, jsonify, request, current_app

from services.humanization_service import HumanizationService


humanization_bp = Blueprint("humanization", __name__)


@humanization_bp.route("/humanize", methods=["POST"])
def humanize_text():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be a JSON object"
        }), 400

    client_id = data.get("client_id")
    text = data.get("text")
    model_id = data.get("model_id")
    prompt_id = data.get("prompt_id")
    max_tokens = data.get("max_tokens", 500)

    if not isinstance(client_id, str) or not client_id.strip():
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "status": "error",
            "message": "Text is required"
        }), 400

    if not isinstance(model_id, int) or isinstance(model_id, bool):
        return jsonify({
            "status": "error",
            "message": "Valid model ID is required"
        }), 400

    if not isinstance(prompt_id, int) or isinstance(prompt_id, bool):
        return jsonify({
            "status": "error",
            "message": "Valid prompt ID is required"
        }), 400

    if (
        not isinstance(max_tokens, int)
        or isinstance(max_tokens, bool)
        or max_tokens <= 0
    ):
        return jsonify({
            "status": "error",
            "message": "Max tokens must be a positive integer"
        }), 400

    try:
        service = HumanizationService()

        result = service.humanize(
            text=text,
            model_id=model_id,
            prompt_id=prompt_id,
            client_id=client_id,
            max_tokens=max_tokens
        )

        return jsonify({
            "status": "success",
            "message": "Text humanized successfully",
            "result": result
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except LookupError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 404

    except Exception:
        current_app.logger.exception("Humanization failed")

        return jsonify({
            "status": "error",
            "message": "AI provider request failed"
        }), 502
