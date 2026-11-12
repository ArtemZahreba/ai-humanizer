
from unittest.mock import patch

from app import app


def test_get_history_detail_api():
    client = app.test_client()

    expected_history = {
        "id": 1,
        "original_text": "Original text",
        "result_text": "Humanized text",
        "model_id": "deepseek-ai/DeepSeek-R1:novita",
        "prompt_id": 2,
        "prompt_snapshot": "Rewrite naturally.",
        "processing_time": 1.25,
        "created_at": "2026-11-12T15:30:00"
    }

    with patch(
        "routes.history.HistoryService.get_history_by_id",
        return_value=expected_history
    ) as history_mock:

        response = client.get(
            "/api/history/1",
            query_string={"client_id": "test_client"}
        )

        history_mock.assert_called_once_with(
            history_id=1,
            client_id="test_client"
        )

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["history"]["id"] == 1
    assert data["history"]["prompt_snapshot"] == "Rewrite naturally."

    print("SUCCESS: Get history detail API test passed!")


def test_history_detail_not_found():
    client = app.test_client()

    with patch(
        "routes.history.HistoryService.get_history_by_id",
        return_value=None
    ):
        response = client.get(
            "/api/history/999",
            query_string={"client_id": "test_client"}
        )

    assert response.status_code == 404
    assert response.get_json()["message"] == "History record not found"

    print("SUCCESS: History detail not found test passed!")


def test_history_detail_missing_client_id():
    client = app.test_client()

    response = client.get("/api/history/1")

    assert response.status_code == 400

    print("SUCCESS: Missing client ID test passed!")


def test_history_detail_service_error():
    client = app.test_client()

    with patch(
        "routes.history.HistoryService.get_history_by_id",
        side_effect=ValueError("Client ID is required")
    ):
        response = client.get(
            "/api/history/1",
            query_string={"client_id": "test_client"}
        )

    assert response.status_code == 400

    print("SUCCESS: History detail service error test passed!")


def run_tests():
    test_get_history_detail_api()
    test_history_detail_not_found()
    test_history_detail_missing_client_id()
    test_history_detail_service_error()

    print("\nAll History Detail API tests passed!")


if __name__ == "__main__":
    run_tests()
