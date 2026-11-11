
from pathlib import Path

from flask import Flask

from config import Config
from database.db import db

# Import database models
from database.models import Prompt, AIModel, HumanizationHistory
from database.seed import seed_default_prompts

# Import blueprints
from routes.main import main_bp
from routes.humanization import humanization_bp
from routes.prompts import prompts_bp
from routes.history import history_bp
from routes.models import models_bp


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True
    )

    # Load configuration
    app.config.from_object(Config)

    # Create instance directory
    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    app.register_blueprint(
        humanization_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        prompts_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        history_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        models_bp,
        url_prefix="/api"
    )

    # Create database tables and seed default prompts
    with app.app_context():
        db.create_all()
        seed_default_prompts()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=app.config["DEBUG"]
    )
