
from database.db import db
from database.models import Prompt


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
