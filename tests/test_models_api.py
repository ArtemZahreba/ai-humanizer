
from app import app


def test_get_models():
    with app.test_client() as client:
        response = client.get("/api/models")

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "success"
        assert data["count"] == 3


def test_get_model():
    with app.test_client() as client:
        response = client.get("/api/models/1")

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "success"
        assert data["model"]["name"] == "DeepSeek R1"


def test_get_nonexistent_model():
    with app.test_client() as client:
        response = client.get("/api/models/999")

        assert response.status_code == 404

        data = response.get_json()

        assert data["status"] == "error"
