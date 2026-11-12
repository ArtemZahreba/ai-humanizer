
from sqlalchemy import or_

from database.db import db
from database.models import Prompt


class PromptService:
    """Service for managing default and custom prompts."""

    @staticmethod
    def get_all_prompts(client_id: str):
        """Return default prompts and custom prompts of a client."""

        return Prompt.query.filter(
            or_(
                Prompt.is_default.is_(True),
                Prompt.client_id == client_id
            )
        ).order_by(Prompt.id).all()

    @staticmethod
    def get_default_prompts():
        """Return all default prompts."""

        return Prompt.query.filter_by(
            is_default=True
        ).order_by(Prompt.id).all()

    @staticmethod
    def get_custom_prompts(client_id: str):
        """Return custom prompts belonging to a client."""

        return Prompt.query.filter_by(
            client_id=client_id,
            is_default=False
        ).order_by(Prompt.id).all()

    @staticmethod
    def get_prompt_by_id(prompt_id: int, client_id: str = None):
        """Find a default prompt or a client's own custom prompt."""

        prompt = db.session.get(Prompt, prompt_id)

        if not prompt:
            return None

        if prompt.is_default:
            return prompt

        if client_id and prompt.client_id == client_id:
            return prompt

        return None

    @staticmethod
    def create_prompt(
        client_id: str,
        name: str,
        content: str,
        category: str,
        description: str = None
    ):
        """Create a custom prompt."""

        if not client_id or not client_id.strip():
            raise ValueError("Client ID is required")

        if not name or not name.strip():
            raise ValueError("Prompt name is required")

        if not content or not content.strip():
            raise ValueError("Prompt content is required")

        if not category or not category.strip():
            raise ValueError("Prompt category is required")

        prompt = Prompt(
            client_id=client_id,
            name=name.strip(),
            description=description.strip() if description else None,
            content=content.strip(),
            category=category.strip(),
            is_default=False
        )

        db.session.add(prompt)
        db.session.commit()

        return prompt

    @staticmethod
    def update_prompt(
        prompt_id: int,
        client_id: str,
        name: str = None,
        content: str = None,
        category: str = None,
        description: str = None
    ):
        """Update a client's custom prompt."""

        prompt = PromptService.get_prompt_by_id(
            prompt_id,
            client_id
        )

        if not prompt or prompt.is_default:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("Prompt name cannot be empty")
            prompt.name = name.strip()

        if content is not None:
            if not content.strip():
                raise ValueError("Prompt content cannot be empty")
            prompt.content = content.strip()

        if category is not None:
            if not category.strip():
                raise ValueError("Prompt category cannot be empty")
            prompt.category = category.strip()

        if description is not None:
            prompt.description = description.strip() or None

        db.session.commit()

        return prompt

    @staticmethod
    def delete_prompt(prompt_id: int, client_id: str):
        """Delete a client's custom prompt."""

        prompt = PromptService.get_prompt_by_id(
            prompt_id,
            client_id
        )

        if not prompt or prompt.is_default:
            return False

        db.session.delete(prompt)
        db.session.commit()

        return True
