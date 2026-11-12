from app import app
from services.prompt_service import PromptService


def test_prompt_service():
    with app.app_context():
        client_a = "test_client_a"
        client_b = "test_client_b"

        # Отримуємо стандартні промпти
        defaults = PromptService.get_default_prompts()
        assert len(defaults) > 0
        print("Default prompts: OK")

        # Створюємо користувацький промпт
        prompt = PromptService.create_prompt(
            client_id=client_a,
            name="Test Prompt",
            content="Rewrite the text naturally.",
            category="general",
            description="Test description"
        )
        print("Create prompt: OK")

        # Перевіряємо доступ власника
        found = PromptService.get_prompt_by_id(prompt.id, client_a)
        assert found is not None
        print("Prompt ownership: OK")

        # Перевіряємо ізоляцію між клієнтами
        hidden = PromptService.get_prompt_by_id(prompt.id, client_b)
        assert hidden is None
        print("Client isolation: OK")

        # Оновлюємо промпт
        updated = PromptService.update_prompt(
            prompt_id=prompt.id,
            client_id=client_a,
            name="Updated Test Prompt"
        )
        assert updated.name == "Updated Test Prompt"
        print("Update prompt: OK")

        # Перевіряємо захист стандартних промптів
        default_prompt = defaults[0]

        updated_default = PromptService.update_prompt(
            prompt_id=default_prompt.id,
            client_id=client_a,
            name="Changed Default"
        )
        assert updated_default is None

        deleted_default = PromptService.delete_prompt(
            default_prompt.id,
            client_a
        )
        assert deleted_default is False
        print("Default prompts protection: OK")

        # Видаляємо тестовий промпт
        deleted = PromptService.delete_prompt(prompt.id, client_a)
        assert deleted is True
        print("Delete prompt: OK")


if __name__ == "__main__":
    test_prompt_service()