# 6. Інтеграція зі штучним інтелектом

## 6.1. Загальна схема
Застосунок використовує Hugging Face Inference Router через OpenAI-сумісний API. Для HTTP-взаємодії використовується OpenAI Python SDK.

Endpoint: `https://router.huggingface.co/v1`.

Токен читається з environment variable `HF_TOKEN`.

## 6.2. Моделі

| Назва | Ідентифікатор | Провайдер |
|---|---|---|
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1:novita` | novita |
| Llama 3.1 8B Instruct | `meta-llama/Llama-3.1-8B-Instruct:novita` | novita |
| GPT-OSS 120B | `openai/gpt-oss-120b:groq` | groq |

## 6.3. Формування prompt
`HumanizationService` об'єднує:
1. Вміст обраного промпту.
2. Загальні правила формату відповіді (`OUTPUT_FORMAT_RULES`).
3. Початковий текст користувача.

Правила вимагають повертати лише переформульований текст, не додавати вступів, пояснень, підсумків або Markdown-цитат і зберігати початковий зміст та важливу інформацію.

## 6.4. Виклик моделі
`HuggingFaceService.generate_text()` викликає `client.chat.completions.create()`, передаючи ID моделі, повідомлення з prompt і `max_tokens`. Сервіс повертає текст першого вибору. Порожній результат вважається помилкою; запис успішної операції в історію в такому разі не створюється.

## 6.5. Обробка помилок

| Помилка SDK | HTTP-статус |
|---|---|
| `RateLimitError` | 429 |
| `NotFoundError` | 503 |
| `AuthenticationError`, `PermissionDeniedError` | 502 |
| `APIConnectionError`, `APITimeoutError` | 503 |
| Інші `APIStatusError` | 502 |

Помилки перетворюються на `HuggingFaceServiceError` і обробляються route гуманізації.

## 6.6. Налаштування
Приклад `.env.example`:

```env
HF_TOKEN=your_huggingface_token
FLASK_DEBUG=True
```

Реальний токен не слід додавати до Git. `.gitignore` виключає `.env` та інші локальні env-файли, залишаючи `.env.example`.
