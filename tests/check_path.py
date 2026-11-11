from app import app
from pathlib import Path

with app.app_context():
    print("Instance path:", app.instance_path)
    print(
        "Database URI:",
        app.config["SQLALCHEMY_DATABASE_URI"]
    )

    db_path = Path(app.instance_path) / "app.db"

    print("Expected database path:", db_path)
    print("Database exists:", db_path.exists())