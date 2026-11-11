
from database.db import db
from database.models import Prompt, AIModel


DEFAULT_PROMPTS = [
    {
        "name": "Natural",
        "description": "Natural and fluent language.",
        "category": "natural",
        "content": (
            "Rewrite the provided text in clear, natural and fluent language. "
            "Vary sentence structure while preserving the original meaning, "
            "facts and important details. Avoid unnecessary repetition."
        )
    },
    {
        "name": "Academic",
        "description": "Academic writing style.",
        "category": "academic",
        "content": (
            "Rewrite the text using an academic writing style. "
            "Maintain clarity, logical structure and precise terminology. "
            "Preserve the original meaning and factual accuracy."
        )
    },
    {
        "name": "Professional",
        "description": "Professional and business communication.",
        "category": "professional",
        "content": (
            "Rewrite the text in a professional and polished style. "
            "Use clear language, appropriate terminology and logical "
            "transitions while preserving the original meaning."
        )
    },
    {
        "name": "Casual",
        "description": "Conversational writing style.",
        "category": "casual",
        "content": (
            "Rewrite the text in a friendly and conversational tone. "
            "Use natural expressions and varied sentence structures. "
            "Preserve the original meaning and avoid adding new information."
        )
    },
    {
        "name": "Simple",
        "description": "Simple and easy-to-understand language.",
        "category": "simple",
        "content": (
            "Rewrite the text using simple and accessible language. "
            "Replace unnecessarily complex constructions with clearer "
            "alternatives while preserving the original meaning."
        )
    },
    {
        "name": "Creative",
        "description": "Creative and expressive writing.",
        "category": "creative",
        "content": (
            "Rewrite the text using expressive and varied language. "
            "Improve readability and flow while preserving the original "
            "meaning, facts and intended message."
        )
    }
]


DEFAULT_MODELS = [
    {
        "model_id": "deepseek-ai/DeepSeek-R1:novita",
        "name": "DeepSeek R1",
        "description": "Reasoning model for complex text processing.",
        "provider": "novita",
    },
    {
        "model_id": "meta-llama/Llama-3.1-8B-Instruct:novita",
        "name": "Llama 3.1 8B Instruct",
        "description": "Instruction-following language model.",
        "provider": "novita",
    },
    {
        "model_id": "openai/gpt-oss-120b:groq",
        "name": "GPT-OSS 120B",
        "description": "Large language model for text generation.",
        "provider": "groq",
    },
]




def seed_default_prompts():
    """Insert default prompts if they do not exist."""

    for prompt_data in DEFAULT_PROMPTS:
        existing_prompt = Prompt.query.filter_by(
            name=prompt_data["name"],
            is_default=True
        ).first()

        if existing_prompt:
            continue

        prompt = Prompt(
            client_id=None,
            name=prompt_data["name"],
            description=prompt_data["description"],
            category=prompt_data["category"],
            content=prompt_data["content"],
            is_default=True
        )

        db.session.add(prompt)

    db.session.commit()


def seed_default_models():
    """Add default AI models to the database."""

    for model_data in DEFAULT_MODELS:
        existing_model = AIModel.query.filter_by(
            model_id=model_data["model_id"]
        ).first()

        if existing_model:
            continue

        model = AIModel(
            model_id=model_data["model_id"],
            name=model_data["name"],
            description=model_data["description"],
            provider=model_data["provider"],
            is_active=True
        )

        db.session.add(model)

    db.session.commit()
