
from app import app
from services.model_service import ModelService


with app.app_context():

    print("=== ALL MODELS ===")

    models = ModelService.get_all_models()

    for model in models:
        print(f"{model.id}. {model.name}")

    print("\n=== ACTIVE MODELS ===")

    active_models = ModelService.get_active_models()

    for model in active_models:
        print(f"{model.id}. {model.name}")

    print("\n=== MODEL BY DATABASE ID ===")

    model = ModelService.get_model_by_id(1)

    if model:
        print(model.name)
    else:
        print("Model not found")

    print("\n=== MODEL BY HUGGING FACE ID ===")

    model = ModelService.get_model_by_model_id(
        "deepseek-ai/DeepSeek-R1:novita"
    )

    if model:
        print(model.name)
    else:
        print("Model not found")
