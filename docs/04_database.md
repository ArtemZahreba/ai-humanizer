# 4. Проєктування бази даних

## 4.1. Загальні відомості
Використовується SQLite, доступ до якої здійснюється через SQLAlchemy ORM. Моделі описані в `database/models.py`. За замовчуванням у конфігурації вказано `sqlite:///app.db`.

## 4.2. Таблиця `prompts`

| Поле | Тип / властивість | Призначення |
|---|---|---|
| `id` | Integer, PK | Ідентифікатор |
| `client_id` | String(64), nullable, index | Власник; `NULL` для стандартних промптів |
| `name` | String(100) | Назва |
| `description` | String(255) | Опис |
| `content` | Text | Інструкція для AI |
| `category` | String(50) | Категорія |
| `is_default` | Boolean | Ознака стандартного промпту |
| `created_at` | DateTime | Дата створення |

## 4.3. Таблиця `ai_models`

| Поле | Тип / властивість | Призначення |
|---|---|---|
| `id` | Integer, PK | Внутрішній ID |
| `model_id` | String(255), unique | ID моделі провайдера |
| `name` | String(100) | Назва |
| `description` | Text | Опис |
| `provider` | String(100) | Провайдер |
| `is_active` | Boolean | Активність |
| `created_at` | DateTime | Дата створення |

## 4.4. Таблиця `humanization_history`

| Поле | Тип / властивість | Призначення |
|---|---|---|
| `id` | Integer, PK | Ідентифікатор запису |
| `client_id` | String(64), NOT NULL, index | Ідентифікатор клієнта |
| `original_text` | Text | Початковий текст |
| `result_text` | Text | Результат |
| `model_id` | String(255) | ID використаної моделі |
| `prompt_id` | Integer, FK, nullable | Посилання на промпт |
| `prompt_snapshot` | Text | Копія промпту на момент операції |
| `processing_time` | Float | Час обробки |
| `created_at` | DateTime, index | Дата створення |

## 4.5. Зв'язки
`humanization_history.prompt_id` посилається на `prompts.id`. Для зовнішнього ключа задано `ON DELETE SET NULL`: після видалення промпту запис історії зберігається, а його `prompt_id` стає `NULL`.

`humanization_history.model_id` — текстове поле, а не зовнішній ключ на `ai_models`.

## 4.6. Початкове наповнення
`seed_default_prompts()` додає шість стандартних промптів: Natural, Academic, Professional, Casual, Simple, Creative. `seed_default_models()` додає DeepSeek R1 (`deepseek-ai/DeepSeek-R1:novita`), Llama 3.1 8B Instruct (`meta-llama/Llama-3.1-8B-Instruct:novita`) та GPT-OSS 120B (`openai/gpt-oss-120b:groq`), якщо відповідні записи ще не існують.

## 4.7. Особливості
Таблиці створюються через `db.create_all()`, міграції не налаштовані. `client_id` є прикладним фільтром даних, а не автентифікованою ідентичністю. `prompt_snapshot` зберігає використану інструкцію навіть після зміни чи видалення промпту.
