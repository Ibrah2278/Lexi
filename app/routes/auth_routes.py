from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models import User, Favorite, SearchHistory

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


# =========================================================
# REGISTER USER
# POST /api/users
# =========================================================
@auth_bp.route("/users", methods=["POST"])
def register_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not name or not email or not password:
            return jsonify({
                "success": False,
                "message": "Nom, email et mot de passe sont obligatoires"
            }), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Un utilisateur avec cet email existe déjà"
            }), 409

        new_user = User(
            name=name,
            email=email
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Utilisateur créé avec succès",
            "user": new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la création de l'utilisateur",
            "error": str(e)
        }), 500


# =========================================================
# LOGIN
# POST /api/login
# =========================================================
@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email et mot de passe sont obligatoires"
            }), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({
                "success": False,
                "message": "Email ou mot de passe incorrect"
            }), 401

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "success": True,
            "message": "Connexion réussie",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la connexion",
            "error": str(e)
        }), 500


# =========================================================
# GET CURRENT USER PROFILE
# GET /api/me
# =========================================================
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({
                "success": False,
                "message": "Utilisateur introuvable"
            }), 404

        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération du profil",
            "error": str(e)
        }), 500


# =========================================================
# GET USER BY ID
# GET /api/users/<id>
# =========================================================
@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "success": False,
                "message": "Utilisateur introuvable"
            }), 404

        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération de l'utilisateur",
            "error": str(e)
        }), 500


# =========================================================
# GET ALL USERS (optionnel debug/admin simple)
# GET /api/users
# =========================================================
@auth_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = User.query.order_by(User.created_at.desc()).all()

        return jsonify({
            "success": True,
            "count": len(users),
            "users": [user.to_dict() for user in users]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération des utilisateurs",
            "error": str(e)
        }), 500