from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Article

articles_bp = Blueprint("articles", __name__, url_prefix="/api/articles")


# =========================================================
# GET ALL ARTICLES
# GET /api/articles
# Query params:
# - category=femme|enfant|famille
# - q=motclé
# =========================================================
@articles_bp.route("", methods=["GET"])
def get_articles():
    try:
        category = request.args.get("category", "").strip().lower()
        q = request.args.get("q", "").strip().lower()

        query = Article.query

        if category:
            query = query.filter(Article.category == category)

        if q:
            query = query.filter(
                (Article.title.ilike(f"%{q}%")) |
                (Article.content.ilike(f"%{q}%"))
            )

        articles = query.order_by(Article.created_at.desc()).all()

        return jsonify({
            "success": True,
            "count": len(articles),
            "articles": [article.to_dict(include_content=False) for article in articles]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération des articles",
            "error": str(e)
        }), 500


# =========================================================
# GET ARTICLE BY ID
# GET /api/articles/<id>
# =========================================================
@articles_bp.route("/<int:article_id>", methods=["GET"])
def get_article_by_id(article_id):
    try:
        article = Article.query.get(article_id)

        if not article:
            return jsonify({
                "success": False,
                "message": "Article introuvable"
            }), 404

        return jsonify({
            "success": True,
            "article": article.to_dict(include_content=True)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération de l'article",
            "error": str(e)
        }), 500


# =========================================================
# SEARCH ARTICLES
# POST /api/articles/search
# Body:
# {
#   "keyword": "violence"
# }
# =========================================================
@articles_bp.route("/search", methods=["POST"])
def search_articles():
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

        return jsonify({
            "success": True,
            "count": len(articles),
            "keyword": keyword,
            "articles": [article.to_dict(include_content=False) for article in articles]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la recherche des articles",
            "error": str(e)
        }), 500


# =========================================================
# CREATE ARTICLE
# POST /api/articles
# =========================================================
@articles_bp.route("", methods=["POST"])
def create_article():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        category = data.get("category", "").strip().lower()

        allowed_categories = ["femme", "enfant", "famille"]

        if not title or not content or not category:
            return jsonify({
                "success": False,
                "message": "Titre, contenu et catégorie sont obligatoires"
            }), 400

        if category not in allowed_categories:
            return jsonify({
                "success": False,
                "message": f"Catégorie invalide. Valeurs autorisées : {allowed_categories}"
            }), 400

        new_article = Article(
            title=title,
            content=content,
            category=category
        )

        db.session.add(new_article)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Article créé avec succès",
            "article": new_article.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la création de l'article",
            "error": str(e)
        }), 500


# =========================================================
# UPDATE ARTICLE
# PUT /api/articles/<id>
# =========================================================
@articles_bp.route("/<int:article_id>", methods=["PUT"])
def update_article(article_id):
    try:
        article = Article.query.get(article_id)

        if not article:
            return jsonify({
                "success": False,
                "message": "Article introuvable"
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        title = data.get("title")
        content = data.get("content")
        category = data.get("category")

        allowed_categories = ["femme", "enfant", "famille"]

        if title is not None:
            article.title = title.strip()

        if content is not None:
            article.content = content.strip()

        if category is not None:
            category = category.strip().lower()
            if category not in allowed_categories:
                return jsonify({
                    "success": False,
                    "message": f"Catégorie invalide. Valeurs autorisées : {allowed_categories}"
                }), 400
            article.category = category

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Article mis à jour avec succès",
            "article": article.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la mise à jour de l'article",
            "error": str(e)
        }), 500


# =========================================================
# DELETE ARTICLE
# DELETE /api/articles/<id>
# =========================================================
@articles_bp.route("/<int:article_id>", methods=["DELETE"])
def delete_article(article_id):
    try:
        article = Article.query.get(article_id)

        if not article:
            return jsonify({
                "success": False,
                "message": "Article introuvable"
            }), 404

        db.session.delete(article)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Article supprimé avec succès"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la suppression de l'article",
            "error": str(e)
        }), 500