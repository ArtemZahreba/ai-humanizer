from app import app


def test_create_prompt_api():
    client = app.test_client()

    # Тестові дані
    payload = {
        "client_id": "test_client_post",
        "name": "Test Natural Writing",
        "description": "Test description",
        "content": "Rewrite text naturally.",
        "category": "general"
    }

    # Створення промпту
    response = client.post(
        "/api/prompts",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["status"] == "success"
    assert data["prompt"]["name"] == payload["name"]
    assert data["prompt"]["content"] == payload["content"]
    assert data["prompt"]["category"] == payload["category"]

    prompt_id = data["prompt"]["id"]

    print("POST /api/prompts: OK")

    # Перевіряємо, чи промпт зберігся в БД
    response = client.get(
        f"/api/prompts/{prompt_id}?client_id=test_client_post"
    )

    assert response.status_code == 200
    print("Prompt persistence: OK")

    # Перевірка відсутності обов'язкових полів
    response = client.post(
        "/api/prompts",
        json={
            "client_id": "test_client_post",
            "name": "",
            "content": "Test content",
            "category": "general"
        }
    )

    assert response.status_code == 400
    print("Required fields validation: OK")

    # Перевірка неправильного формату JSON
    response = client.post(
        "/api/prompts",
        json=[]
    )

    assert response.status_code == 400
    print("Invalid JSON structure: OK")

    # Видаляємо тестовий промпт через сервіс
    from services.prompt_service import PromptService

    with app.app_context():
        deleted = PromptService.delete_prompt(
            prompt_id,
            "test_client_post"
        )
        assert deleted is True

    print("Test data cleanup: OK")


if __name__ == "__main__":
    test_create_prompt_api()