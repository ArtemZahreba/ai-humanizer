from app import app
from services.prompt_service import PromptService


def test_delete_prompt_api():
    client = app.test_client()

    client_id = "test_client_delete"
    other_client_id = "another_test_client"

    with app.app_context():
        # Створюємо два тестові промпти
        prompt = PromptService.create_prompt(
            client_id=client_id,
            name="Prompt To Delete",
            content="Test content",
            category="general"
        )

        other_prompt = PromptService.create_prompt(
            client_id=client_id,
            name="Protected Prompt",
            content="Protected content",
            category="general"
        )

        prompt_id = prompt.id
        other_prompt_id = other_prompt.id

        default_prompt_id = PromptService.get_default_prompts()[0].id

    try:
        # 1. Успішне видалення
        response = client.delete(
            f"/api/prompts/{prompt_id}",
            json={"client_id": client_id}
        )

        assert response.status_code == 200
        assert response.get_json()["status"] == "success"

        print("DELETE own prompt: OK")

        # 2. Перевіряємо, що промпт справді видалений
        response = client.get(
            f"/api/prompts/{prompt_id}?client_id={client_id}"
        )

        assert response.status_code == 404

        print("Prompt deletion verification: OK")

        # 3. Спроба видалення чужого промпту
        response = client.delete(
            f"/api/prompts/{other_prompt_id}",
            json={"client_id": other_client_id}
        )

        assert response.status_code == 404

        print("Other client protection: OK")

        # Перевіряємо, що чужий промпт залишився
        response = client.get(
            f"/api/prompts/{other_prompt_id}?client_id={client_id}"
        )

        assert response.status_code == 200

        print("Protected prompt persistence: OK")

        # 4. Спроба видалити стандартний промпт
        response = client.delete(
            f"/api/prompts/{default_prompt_id}",
            json={"client_id": client_id}
        )

        assert response.status_code == 404

        print("Default prompt protection: OK")

        # 5. Відсутній client_id
        response = client.delete(
            f"/api/prompts/{other_prompt_id}",
            json={}
        )

        assert response.status_code == 400

        print("Missing client_id validation: OK")

        # 6. Некоректна структура JSON
        response = client.delete(
            f"/api/prompts/{other_prompt_id}",
            json=[]
        )

        assert response.status_code == 400

        print("Invalid JSON structure: OK")

    finally:
        # Очищення тестових записів
        with app.app_context():
            PromptService.delete_prompt(
                other_prompt_id,
                client_id
            )

            # Якщо перший запис залишився через помилку тесту
            PromptService.delete_prompt(
                prompt_id,
                client_id
            )

        print("Test data cleanup: OK")


if __name__ == "__main__":
    test_delete_prompt_api()