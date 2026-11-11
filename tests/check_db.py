
from app import app
from database.models import Prompt, AIModel, HumanizationHistory
from sqlalchemy import inspect
from database.db import db


with app.app_context():

    print("Database tables:")

    tables = inspect(db.engine).get_table_names()

    for table in tables:
        print(f"- {table}")

    print("\nDefault prompts:")

    prompts = Prompt.query.filter_by(is_default=True).all()

    for prompt in prompts:
        print(f"{prompt.id}. {prompt.name} — {prompt.category}")

    print(f"\nTotal prompts: {len(prompts)}")
    print(f"Total AI models: {AIModel.query.count()}")
    print(f"Total history records: {HumanizationHistory.query.count()}")

    print("\nAI Models:")

    models = AIModel.query.all()

    for model in models:
        print(
            f"{model.id}. {model.name} | "
            f"{model.model_id} | "
            f"Provider: {model.provider} | "
            f"Active: {model.is_active}"
        )

    print(f"\nTotal AI models: {len(models)}")

