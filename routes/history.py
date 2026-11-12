
from flask import Blueprint, jsonify, request, current_app

from services.history_service import HistoryService


history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def get_history():
    client_id = request.args.get("client_id")

    if not client_id or not client_id.strip():
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    try:
        history = HistoryService.get_history(client_id)

        return jsonify({
            "status": "success",
            "count": len(history),
            "history": history
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        from flask import current_app
        current_app.logger.exception("Failed to retrieve history")

        return jsonify({
            "status": "error",
            "message": "Failed to retrieve history"
        }), 500


@history_bp.route("/history/<int:history_id>", methods=["GET"])
def get_history_detail(history_id):
    client_id = request.args.get("client_id")

    if not client_id or not client_id.strip():
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    try:
        history = HistoryService.get_history_by_id(
            history_id=history_id,
            client_id=client_id
        )

        if not history:
            return jsonify({
                "status": "error",
                "message": "History record not found"
            }), 404

        return jsonify({
            "status": "success",
            "history": history
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        from flask import current_app
        current_app.logger.exception("Failed to retrieve history record")

        return jsonify({
            "status": "error",
            "message": "Failed to retrieve history record"
        }), 500

@history_bp.route("/history/<int:history_id>", methods=["DELETE"])
def delete_history(history_id):
    client_id = request.args.get("client_id")

    if not client_id or not client_id.strip():
        return jsonify({
            "status": "error",
            "message": "Client ID is required"
        }), 400

    try:
        deleted = HistoryService.delete_history(
            history_id=history_id,
            client_id=client_id
        )

        if not deleted:
            return jsonify({
                "status": "error",
                "message": "History record not found"
            }), 404

        return jsonify({
            "status": "success",
            "message": "History record deleted successfully"
        }), 200

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        current_app.logger.exception("Failed to delete history record")

        return jsonify({
            "status": "error",
            "message": "Failed to delete history record"
        }), 500