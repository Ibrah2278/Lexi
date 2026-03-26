from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Favorite, User, Article, Guide, Contact

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api/users")


# =========================================================
# GET USER FAVORITES
# GET /api/users/<id>/favorites
# =========================================================
@favorites_bp.route("/<int:user_id>/favorites", methods=["GET"])
@jwt_required()
def get_user_favorites(user_id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != user_id:
            return jsonify({
                "success": False,
                "message": "Accès non autorisé"
            }), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "success": False,
                "message": "Utilisateur introuvable"
            }), 404

        favorites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()

        results = []

        for fav in favorites:
            item_data = None

            if fav.type == "article":
                item = Article.query.get(fav.item_id)
                if item:
                    item_data = item.to_dict(include_content=False)

            elif fav.type == "guide":
                item = Guide.query.get(fav.item_id)
                if item:
                    item_data = item.to_dict(include_content=False)

            elif fav.type == "contact":
                item = Contact.query.get(fav.item_id)
                if item:
                    item_data = item.to_dict()

            if item_data:
                results.append({
                    "favorite_id": fav.id,
                    "type": fav.type,
                    "item_id": fav.item_id,
                    "created_at": fav.created_at.isoformat() if fav.created_at else None,
                    "item": item_data
                })

        return jsonify({
            "success": True,
            "count": len(results),
            "favorites": results
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération des favoris",
            "error": str(e)
        }), 500


# =========================================================
# ADD FAVORITE
# POST /api/users/<id>/favorites
# Body:
# {
#   "type": "article" | "guide" | "contact",
#   "item_id": 1
# }
# =========================================================
@favorites_bp.route("/<int:user_id>/favorites", methods=["POST"])
@jwt_required()
def add_favorite(user_id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != user_id:
            return jsonify({
                "success": False,
                "message": "Accès non autorisé"
            }), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "success": False,
                "message": "Utilisateur introuvable"
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        fav_type = data.get("type", "").strip().lower()
        item_id = data.get("item_id")

        allowed_types = ["article", "guide", "contact"]

        if not fav_type or not item_id:
            return jsonify({
                "success": False,
                "message": "Le type et item_id sont obligatoires"
            }), 400

        if fav_type not in allowed_types:
            return jsonify({
                "success": False,
                "message": f"Type invalide. Valeurs autorisées : {allowed_types}"
            }), 400

        # Vérifier si l'élément existe
        item_exists = False

        if fav_type == "article":
            item_exists = Article.query.get(item_id) is not None
        elif fav_type == "guide":
            item_exists = Guide.query.get(item_id) is not None
        elif fav_type == "contact":
            item_exists = Contact.query.get(item_id) is not None

        if not item_exists:
            return jsonify({
                "success": False,
                "message": "Élément introuvable"
            }), 404

        # Éviter doublon
        existing_favorite = Favorite.query.filter_by(
            user_id=user_id,
            type=fav_type,
            item_id=item_id
        ).first()

        if existing_favorite:
            return jsonify({
                "success": False,
                "message": "Cet élément est déjà dans les favoris"
            }), 409

        new_favorite = Favorite(
            user_id=user_id,
            type=fav_type,
            item_id=item_id
        )

        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Favori ajouté avec succès",
            "favorite": new_favorite.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de l'ajout du favori",
            "error": str(e)
        }), 500


# =========================================================
# DELETE FAVORITE
# DELETE /api/users/<id>/favorites/<favorite_id>
# =========================================================
@favorites_bp.route("/<int:user_id>/favorites/<int:favorite_id>", methods=["DELETE"])
@jwt_required()
def delete_favorite(user_id, favorite_id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != user_id:
            return jsonify({
                "success": False,
                "message": "Accès non autorisé"
            }), 403

        favorite = Favorite.query.filter_by(id=favorite_id, user_id=user_id).first()

        if not favorite:
            return jsonify({
                "success": False,
                "message": "Favori introuvable"
            }), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Favori supprimé avec succès"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la suppression du favori",
            "error": str(e)
        }), 500