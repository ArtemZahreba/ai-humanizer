from flask import Blueprint, jsonify, request

from services.prompt_service import PromptService

prompts_bp = Blueprint("prompts", __name__)


def serialize_prompt(prompt):
    return {
        "id": prompt.id,
        "name": prompt.name,
        "description": prompt.description,
        "content": prompt.content,
        "category": prompt.category,
        "is_default": prompt.is_default
    }


@prompts_bp.route("/prompts", methods=["GET"])
def get_prompts():
    client_id = request.args.get("client_id")

    if not client_id:
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    prompts = PromptService.get_all_prompts(client_id)

    return jsonify({
        "status": "success",
        "count": len(prompts),
        "prompts": [serialize_prompt(prompt) for prompt in prompts]
    }), 200


@prompts_bp.route("/prompts/<int:prompt_id>", methods=["GET"])
def get_prompt(prompt_id):
    client_id = request.args.get("client_id")

    if not client_id:
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    prompt = PromptService.get_prompt_by_id(prompt_id, client_id)

    if not prompt:
        return jsonify({
            "status": "error",
            "message": "Prompt not found"
        }), 404

    return jsonify({
        "status": "success",
        "prompt": serialize_prompt(prompt)
    }), 200