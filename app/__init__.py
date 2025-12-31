from flask import Flask
from .extensions import db, migrate
from .routes import register_blueprints
from config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow}

    return app
