
from uuid import uuid4
from unittest.mock import patch

from app import app


def test_get_history_api():
    client = app.test_client()

    client_id = f"test_{uuid4().hex}"

    expected_history = [
        {
            "id": 1,
            "original_text": "Original text",
            "result_text": "Humanized text",
            "model_id": "deepseek-ai/DeepSeek-R1:novita",
            "prompt_id": 2,
            "processing_time": 1.25,
            "created_at": "2026-11-12T15:30:00"
        }
    ]

    with patch(
        "routes.history.HistoryService.get_history",
        return_value=expected_history
    ) as history_mock:

        response = client.get(
            "/api/history",
            query_string={"client_id": client_id}
        )

        history_mock.assert_called_once_with(client_id)

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["count"] == 1
    assert data["history"][0]["result_text"] == "Humanized text"

    print("SUCCESS: Get history API test passed!")


def test_get_history_missing_client_id():
    client = app.test_client()

    response = client.get("/api/history")

    assert response.status_code == 400
    assert response.get_json()["message"] == "Client ID is required"

    print("SUCCESS: Missing client ID test passed!")


def test_get_history_service_error():
    client = app.test_client()

    with patch(
        "routes.history.HistoryService.get_history",
        side_effect=ValueError("Client ID is required")
    ):
        response = client.get(
            "/api/history",
            query_string={"client_id": "test_client"}
        )

    assert response.status_code == 400

    print("SUCCESS: History service error test passed!")


def run_tests():
    test_get_history_api()
    test_get_history_missing_client_id()
    test_get_history_service_error()

    print("\nAll History API tests passed!")


if __name__ == "__main__":
    run_tests()
