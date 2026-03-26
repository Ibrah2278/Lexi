from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Article, Guide, Contact, SearchHistory

search_bp = Blueprint("search", __name__, url_prefix="/api")


# =========================================================
# GLOBAL SEARCH
# POST /api/search
# Body:
# {
#   "keyword": "violence"
# }
# =========================================================
@search_bp.route("/search", methods=["POST"])
def global_search():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        keyword = data.get("keyword", "").strip().lower()

        if not keyword:
            return jsonify({
                "success": False,
                "message": "Le mot-clé est obligatoire"
            }), 400

        articles = Article.query.filter(
            (Article.title.ilike(f"%{keyword}%")) |
            (Article.content.ilike(f"%{keyword}%")) |
            (Article.category.ilike(f"%{keyword}%"))
        ).order_by(Article.created_at.desc()).all()

        guides = Guide.query.filter(
            (Guide.title.ilike(f"%{keyword}%")) |
            (Guide.content.ilike(f"%{keyword}%")) |
            (Guide.case_type.ilike(f"%{keyword}%"))
        ).order_by(Guide.created_at.desc()).all()

        contacts = Contact.query.filter(
            (Contact.name.ilike(f"%{keyword}%")) |
            (Contact.role.ilike(f"%{keyword}%")) |
            (Contact.specialty.ilike(f"%{keyword}%")) |
            (Contact.address.ilike(f"%{keyword}%"))
        ).order_by(Contact.created_at.desc()).all()

        return jsonify({
            "success": True,
            "keyword": keyword,
            "results": {
                "articles": [article.to_dict(include_content=False) for article in articles],
                "guides": [guide.to_dict(include_content=False) for guide in guides],
                "contacts": [contact.to_dict() for contact in contacts]
            },
            "counts": {
                "articles": len(articles),
                "guides": len(guides),
                "contacts": len(contacts),
                "total": len(articles) + len(guides) + len(contacts)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la recherche",
            "error": str(e)
        }), 500


# =========================================================
# SAVE SEARCH HISTORY
# POST /api/users/<id>/search-history
# Body:
# {
#   "query": "violence conjugale"
# }
# =========================================================
@search_bp.route("/users/<int:user_id>/search-history", methods=["POST"])
@jwt_required()
def save_search_history(user_id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != user_id:
            return jsonify({
                "success": False,
                "message": "Accès non autorisé"
            }), 403

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        query = data.get("query", "").strip()

        if not query:
            return jsonify({
                "success": False,
                "message": "Le champ query est obligatoire"
            }), 400

        new_history = SearchHistory(
            user_id=user_id,
            query=query
        )

        db.session.add(new_history)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Historique enregistré avec succès",
            "history": new_history.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de l'enregistrement de l'historique",
            "error": str(e)
        }), 500


# =========================================================
# GET SEARCH HISTORY
# GET /api/users/<id>/search-history
# =========================================================
@search_bp.route("/users/<int:user_id>/search-history", methods=["GET"])
@jwt_required()
def get_search_history(user_id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != user_id:
            return jsonify({
                "success": False,
                "message": "Accès non autorisé"
            }), 403

        history = SearchHistory.query.filter_by(user_id=user_id).order_by(SearchHistory.created_at.desc()).all()

        return jsonify({
            "success": True,
            "count": len(history),
            "history": [item.to_dict() for item in history]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération de l'historique",
            "error": str(e)
        }), 500