from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Guide

guides_bp = Blueprint("guides", __name__, url_prefix="/api/guides")


# =========================================================
# GET ALL GUIDES
# GET /api/guides
# Query params:
# - case_type=violence|harcelement|abus|litiges
# - q=motclé
# =========================================================
@guides_bp.route("", methods=["GET"])
def get_guides():
    try:
        case_type = request.args.get("case_type", "").strip().lower()
        q = request.args.get("q", "").strip().lower()

        query = Guide.query

        if case_type:
            query = query.filter(Guide.case_type == case_type)

        if q:
            query = query.filter(
                (Guide.title.ilike(f"%{q}%")) |
                (Guide.content.ilike(f"%{q}%"))
            )

        guides = query.order_by(Guide.created_at.desc()).all()

        return jsonify({
            "success": True,
            "count": len(guides),
            "guides": [guide.to_dict(include_content=False) for guide in guides]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération des guides",
            "error": str(e)
        }), 500


# =========================================================
# GET GUIDE BY ID
# GET /api/guides/<id>
# =========================================================
@guides_bp.route("/<int:guide_id>", methods=["GET"])
def get_guide_by_id(guide_id):
    try:
        guide = Guide.query.get(guide_id)

        if not guide:
            return jsonify({
                "success": False,
                "message": "Guide introuvable"
            }), 404

        return jsonify({
            "success": True,
            "guide": guide.to_dict(include_content=True)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération du guide",
            "error": str(e)
        }), 500


# =========================================================
# CREATE GUIDE
# POST /api/guides
# =========================================================
@guides_bp.route("", methods=["POST"])
def create_guide():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        case_type = data.get("case_type", "").strip().lower()

        allowed_case_types = ["violence", "harcelement", "abus", "litiges"]

        if not title or not content or not case_type:
            return jsonify({
                "success": False,
                "message": "Titre, contenu et type de cas sont obligatoires"
            }), 400

        if case_type not in allowed_case_types:
            return jsonify({
                "success": False,
                "message": f"Type de cas invalide. Valeurs autorisées : {allowed_case_types}"
            }), 400

        new_guide = Guide(
            title=title,
            content=content,
            case_type=case_type
        )

        db.session.add(new_guide)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Guide créé avec succès",
            "guide": new_guide.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la création du guide",
            "error": str(e)
        }), 500


# =========================================================
# UPDATE GUIDE
# PUT /api/guides/<id>
# =========================================================
@guides_bp.route("/<int:guide_id>", methods=["PUT"])
def update_guide(guide_id):
    try:
        guide = Guide.query.get(guide_id)

        if not guide:
            return jsonify({
                "success": False,
                "message": "Guide introuvable"
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        title = data.get("title")
        content = data.get("content")
        case_type = data.get("case_type")

        allowed_case_types = ["violence", "harcelement", "abus", "litiges"]

        if title is not None:
            guide.title = title.strip()

        if content is not None:
            guide.content = content.strip()

        if case_type is not None:
            case_type = case_type.strip().lower()
            if case_type not in allowed_case_types:
                return jsonify({
                    "success": False,
                    "message": f"Type de cas invalide. Valeurs autorisées : {allowed_case_types}"
                }), 400
            guide.case_type = case_type

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Guide mis à jour avec succès",
            "guide": guide.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la mise à jour du guide",
            "error": str(e)
        }), 500


# =========================================================
# DELETE GUIDE
# DELETE /api/guides/<id>
# =========================================================
@guides_bp.route("/<int:guide_id>", methods=["DELETE"])
def delete_guide(guide_id):
    try:
        guide = Guide.query.get(guide_id)

        if not guide:
            return jsonify({
                "success": False,
                "message": "Guide introuvable"
            }), 404

        db.session.delete(guide)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Guide supprimé avec succès"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la suppression du guide",
            "error": str(e)
        }), 500