# 5. API

## 5.1. Загальні відомості
API реалізовано на Flask Blueprints із префіксом `/api`. Запити з JSON-тілом мають використовувати `Content-Type: application/json`.

## 5.2. Маршрути

| Метод | URL | Призначення |
|---|---|---|
| GET | `/` | Головна HTML-сторінка |
| GET | `/api/health` | Перевірка API |
| POST | `/api/humanize` | Гуманізація тексту |
| GET | `/api/models` | Активні моделі |
| GET | `/api/models/<model_id>` | Конкретна модель |
| GET | `/api/prompts?client_id=...` | Доступні промпти |
| GET | `/api/prompts/<prompt_id>?client_id=...` | Конкретний промпт |
| POST | `/api/prompts` | Створення промпту |
| PUT | `/api/prompts/<prompt_id>` | Оновлення промпту |
| DELETE | `/api/prompts/<prompt_id>` | Видалення промпту |
| GET | `/api/history?client_id=...` | Історія клієнта |
| GET | `/api/history/<history_id>?client_id=...` | Деталі запису |
| DELETE | `/api/history/<history_id>?client_id=...` | Видалення запису через API |

## 5.3. Гуманізація — `POST /api/humanize`

Приклад запиту:

```json
{
  "client_id": "browser-generated-uuid",
  "text": "Text to humanize",
  "model_id": 1,
  "prompt_id": 2,
  "max_tokens": 500
}
```

`client_id` і `text` мають бути непорожніми рядками; `text` не може перевищувати 5000 символів; `model_id` і `prompt_id` мають бути цілими числами; `max_tokens` — додатне ціле число, за замовчуванням 500.

Успішна відповідь — HTTP 200 з `status: success` та об'єктом `result`. Основні помилки: 400 — некоректні параметри; 404 — модель або промпт не знайдені; 429 — ліміт провайдера; 502/503 — помилка або недоступність AI-сервісу.

## 5.4. Моделі
`GET /api/models` повертає активні моделі з полями `id`, `name`, `model_id`, `description`, `provider`, `is_active`. `GET /api/models/<model_id>` повертає конкретну активну модель або 404.

## 5.5. Промпти
`GET /api/prompts?client_id=...` повертає стандартні промпти та власні промпти клієнта. `GET /api/prompts/<id>?client_id=...` повертає стандартний або власний доступний промпт.

`POST /api/prompts` приймає `client_id`, `name`, `content`, `category` та необов'язковий `description`; успішне створення повертає 201.

`PUT /api/prompts/<id>` приймає `client_id` і принаймні одне поле з `name`, `content`, `category`, `description`. Оновлювати можна лише власний користувацький промпт.

`DELETE /api/prompts/<id>` приймає JSON із `client_id` та видаляє лише власний користувацький промпт.

## 5.6. Історія
`GET /api/history?client_id=...` повертає записи клієнта від найновіших до найстаріших. `GET /api/history/<id>?client_id=...` повертає конкретний запис, якщо він належить клієнту.

`DELETE /api/history/<id>?client_id=...` існує на Backend, але дія видалення не представлена в поточному Frontend.

## 5.7. Health check
`GET /api/health` повертає JSON зі статусом `ok` і повідомленням про роботу API.
