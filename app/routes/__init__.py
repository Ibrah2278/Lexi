# app/routes/__init__.py
from .admin_routes import admin_bp
from .chat_routes import chat_bp
from .juris_routes import juris_bp
from .user_routes import user_bp


def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(juris_bp)
    app.register_blueprint(user_bp)
