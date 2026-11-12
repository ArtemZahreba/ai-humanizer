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

@prompts_bp.route("/prompts", methods=["POST"])
def create_prompt():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be a JSON object"
        }), 400

    client_id = data.get("client_id")
    name = data.get("name")
    content = data.get("content")
    category = data.get("category")
    description = data.get("description")

    # Перевіряємо обов'язкові поля
    required_fields = {
        "client_id": client_id,
        "name": name,
        "content": content,
        "category": category
    }

    for field, value in required_fields.items():
        if not isinstance(value, str) or not value.strip():
            return jsonify({
                "status": "error",
                "message": f"{field} is required"
            }), 400

    if description is not None and not isinstance(description, str):
        return jsonify({
            "status": "error",
            "message": "Description must be a string"
        }), 400

    try:
        prompt = PromptService.create_prompt(
            client_id=client_id,
            name=name,
            content=content,
            category=category,
            description=description
        )

        return jsonify({
            "status": "success",
            "message": "Prompt created successfully",
            "prompt": serialize_prompt(prompt)
        }), 201

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

@prompts_bp.route("/prompts/<int:prompt_id>", methods=["PUT"])
def update_prompt(prompt_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be a JSON object"
        }), 400

    client_id = data.get("client_id")

    if not isinstance(client_id, str) or not client_id.strip():
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    allowed_fields = {"name", "content", "category", "description"}

    # Перевіряємо, чи є поля для оновлення
    update_data = {
        key: value
        for key, value in data.items()
        if key in allowed_fields
    }

    if not update_data:
        return jsonify({
            "status": "error",
            "message": "No fields provided for update"
        }), 400

    # Перевіряємо типи переданих значень
    for field, value in update_data.items():
        if not isinstance(value, str):
            return jsonify({
                "status": "error",
                "message": f"{field} must be a string"
            }), 400

    try:
        prompt = PromptService.update_prompt(
            prompt_id=prompt_id,
            client_id=client_id,
            **update_data
        )

        if not prompt:
            return jsonify({
                "status": "error",
                "message": "Prompt not found"
            }), 404

        return jsonify({
            "status": "success",
            "message": "Prompt updated successfully",
            "prompt": serialize_prompt(prompt)
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

@prompts_bp.route("/prompts/<int:prompt_id>", methods=["DELETE"])
def delete_prompt(prompt_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be a JSON object"
        }), 400

    client_id = data.get("client_id")

    if not isinstance(client_id, str) or not client_id.strip():
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    deleted = PromptService.delete_prompt(
        prompt_id=prompt_id,
        client_id=client_id
    )

    if not deleted:
        return jsonify({
            "status": "error",
            "message": "Prompt not found"
        }), 404

    return jsonify({
        "status": "success",
        "message": "Prompt deleted successfully"
    }), 200