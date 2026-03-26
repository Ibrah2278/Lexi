from .auth_routes import auth_bp
from .articles_routes import articles_bp
from .guides_routes import guides_bp
from .contacts_routes import contacts_bp
from .favorites_routes import favorites_bp
from .search_routes import search_bp
from .admin_routes import admin_bp
from .crud_routes import crud_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(guides_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(crud_bp)