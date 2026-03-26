from flask import Flask
from config import Config
from .extensions import db, migrate, jwt, bcrypt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # =========================================
    # INITIALISATION DES EXTENSIONS
    # =========================================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # =========================================
    # IMPORT DES MODELS (important pour migrations)
    # =========================================
    from . import models

    # =========================================
    # ROUTE TEST
    # =========================================
    @app.route("/")
    def home():
        return {
            "message": "Bienvenue sur l'API EllesAid 🚀",
            "status": "success"
        }, 200

    @app.route("/api/health")
    def health_check():
        return {
            "status": "ok",
            "message": "API EllesAid opérationnelle"
        }, 200

    # =========================================
    # ENREGISTREMENT DES BLUEPRINTS
    # (on les ajoutera juste après)
    # =========================================
    try:
        from .routes import register_blueprints
        register_blueprints(app)
    except Exception as e:
        print(f"[WARNING] Blueprints non chargés pour le moment: {e}")

    return app