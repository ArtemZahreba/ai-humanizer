from app import app


def test_prompts_api():
    client = app.test_client()

    # Отримуємо стандартні промпти
    response = client.get(
        "/api/prompts?client_id=test_client_a"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert data["count"] > 0
    assert len(data["prompts"]) == data["count"]

    print("GET /api/prompts: OK")

    # Перевіряємо отримання конкретного промпту
    prompt_id = data["prompts"][0]["id"]

    response = client.get(
        f"/api/prompts/{prompt_id}?client_id=test_client_a"
    )

    assert response.status_code == 200

    prompt_data = response.get_json()["prompt"]

    assert prompt_data["id"] == prompt_id

    print("GET /api/prompts/<id>: OK")

    # Перевіряємо запит без client_id
    response = client.get("/api/prompts")

    assert response.status_code == 400

    print("Missing client_id validation: OK")

    # Перевіряємо неіснуючий промпт
    response = client.get(
        "/api/prompts/999999?client_id=test_client_a"
    )

    assert response.status_code == 404

    print("Unknown prompt handling: OK")


if __name__ == "__main__":
    test_prompts_api()