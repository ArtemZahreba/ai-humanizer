from app import app
from services.prompt_service import PromptService


def test_update_prompt_api():
    client = app.test_client()

    client_id = "test_client_put"

    # Створюємо тестовий промпт
    with app.app_context():
        prompt = PromptService.create_prompt(
            client_id=client_id,
            name="Original Prompt",
            content="Original content",
            category="general",
            description="Original description"
        )

        prompt_id = prompt.id

        defaults = PromptService.get_default_prompts()
        default_prompt_id = defaults[0].id

    try:
        # 1. Повне оновлення
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "client_id": client_id,
                "name": "Updated Prompt",
                "content": "Updated content",
                "category": "academic",
                "description": "Updated description"
            }
        )

        assert response.status_code == 200

        data = response.get_json()
        assert data["status"] == "success"
        assert data["prompt"]["name"] == "Updated Prompt"
        assert data["prompt"]["content"] == "Updated content"

        print("Full update: OK")

        # 2. Часткове оновлення
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "client_id": client_id,
                "name": "Partially Updated Prompt"
            }
        )

        assert response.status_code == 200

        data = response.get_json()
        assert data["prompt"]["name"] == "Partially Updated Prompt"
        assert data["prompt"]["content"] == "Updated content"

        print("Partial update: OK")

        # 3. Спроба редагування чужого промпту
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "client_id": "another_client",
                "name": "Unauthorized Update"
            }
        )

        assert response.status_code == 404
        print("Other client protection: OK")

        # 4. Спроба редагування стандартного промпту
        response = client.put(
            f"/api/prompts/{default_prompt_id}",
            json={
                "client_id": client_id,
                "name": "Changed Default"
            }
        )

        assert response.status_code == 404
        print("Default prompt protection: OK")

        # 5. Відсутній client_id
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "name": "Missing Client"
            }
        )

        assert response.status_code == 400
        print("Missing client_id validation: OK")

        # 6. Відсутні поля для оновлення
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "client_id": client_id
            }
        )

        assert response.status_code == 400
        print("Empty update validation: OK")

        # 7. Порожня назва
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "client_id": client_id,
                "name": ""
            }
        )

        assert response.status_code == 400
        print("Empty field validation: OK")

        # 8. Некоректний тип даних
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json={
                "client_id": client_id,
                "name": 123
            }
        )

        assert response.status_code == 400
        print("Invalid field type validation: OK")

        # 9. Некоректна структура JSON
        response = client.put(
            f"/api/prompts/{prompt_id}",
            json=[]
        )

        assert response.status_code == 400
        print("Invalid JSON structure: OK")

    finally:
        # Прибираємо тестовий запис навіть у разі помилки
        with app.app_context():
            PromptService.delete_prompt(prompt_id, client_id)

        print("Test data cleanup: OK")


if __name__ == "__main__":
    test_update_prompt_api()