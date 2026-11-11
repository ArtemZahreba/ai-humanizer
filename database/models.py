
from datetime import datetime, timezone

from database.db import db


class Prompt(db.Model):
    """Model for default and custom prompts."""

    __tablename__ = "prompts"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.String(64), nullable=True, index=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    is_default = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class AIModel(db.Model):
    """Model for available Hugging Face models."""

    __tablename__ = "ai_models"

    id = db.Column(db.Integer, primary_key=True)

    model_id = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    provider = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class HumanizationHistory(db.Model):
    """Model for humanization history."""

    __tablename__ = "humanization_history"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.String(64),
        nullable=False,
        index=True
    )

    original_text = db.Column(db.Text, nullable=False)
    result_text = db.Column(db.Text, nullable=False)

    model_id = db.Column(db.String(255), nullable=False)

    prompt_id = db.Column(
        db.Integer,
        db.ForeignKey("prompts.id", ondelete="SET NULL"),
        nullable=True
    )

    prompt_snapshot = db.Column(db.Text, nullable=False)

    processing_time = db.Column(db.Float, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    prompt = db.relationship(
        "Prompt",
        backref=db.backref("history_records", lazy=True)
    )
