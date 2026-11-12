
from unittest.mock import patch

from app import app


def test_successful_humanization():
    client = app.test_client()

    payload = {
        "client_id": "test_client",
        "text": "This is an original text.",
        "model_id": 1,
        "prompt_id": 2,
        "max_tokens": 500
    }

    expected_result = {
        "original_text": "This is an original text.",
        "result_text": "This is a humanized text.",
        "model_id": "deepseek-ai/DeepSeek-R1:novita",
        "prompt_id": 2,
        "processing_time": 1.25
    }

    with patch("routes.humanization.HumanizationService") as service_mock:
        service_mock.return_value.humanize.return_value = expected_result

        response = client.post("/api/humanize", json=payload)

        service_mock.return_value.humanize.assert_called_once_with(
            text=payload["text"],
            model_id=payload["model_id"],
            prompt_id=payload["prompt_id"],
            client_id=payload["client_id"],
            max_tokens=payload["max_tokens"]
        )

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["result"]["result_text"] == "This is a humanized text."

    print("SUCCESS: Humanization API test passed!")


def test_missing_text():
    client = app.test_client()

    payload = {
        "client_id": "test_client",
        "model_id": 1,
        "prompt_id": 2
    }

    response = client.post("/api/humanize", json=payload)

    assert response.status_code == 400
    assert response.get_json()["message"] == "Text is required"

    print("SUCCESS: Missing text test passed!")


def test_invalid_model_id():
    client = app.test_client()

    payload = {
        "client_id": "test_client",
        "text": "Some text",
        "model_id": "invalid",
        "prompt_id": 2
    }

    response = client.post("/api/humanize", json=payload)

    assert response.status_code == 400

    print("SUCCESS: Invalid model ID test passed!")


def test_prompt_not_found():
    client = app.test_client()

    payload = {
        "client_id": "test_client",
        "text": "Some text",
        "model_id": 1,
        "prompt_id": 999
    }

    with patch("routes.humanization.HumanizationService") as service_mock:
        service_mock.return_value.humanize.side_effect = LookupError(
            "Prompt not found"
        )

        response = client.post("/api/humanize", json=payload)

    assert response.status_code == 404
    assert response.get_json()["message"] == "Prompt not found"

    print("SUCCESS: Prompt not found test passed!")


def test_ai_provider_error():
    client = app.test_client()

    payload = {
        "client_id": "test_client",
        "text": "Some text",
        "model_id": 1,
        "prompt_id": 2
    }

    with patch("routes.humanization.HumanizationService") as service_mock:
        service_mock.return_value.humanize.side_effect = Exception(
            "Provider unavailable"
        )

        response = client.post("/api/humanize", json=payload)

    assert response.status_code == 502
    assert response.get_json()["message"] == "AI provider request failed"

    print("SUCCESS: AI provider error test passed!")


def run_tests():
    test_successful_humanization()
    test_missing_text()
    test_invalid_model_id()
    test_prompt_not_found()
    test_ai_provider_error()

    print("\nAll Humanization API tests passed!")


if __name__ == "__main__":
    run_tests()
