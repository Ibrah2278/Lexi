from flask import Blueprint, request, redirect, session, url_for, flash
from app.extensions import db
from app.models import Article, Guide, Contact

crud_bp = Blueprint("crud", __name__, url_prefix="/admin")

# ---------------------------------------------------------
# Vérification simple si admin connecté
# ---------------------------------------------------------
def is_admin_logged_in():
    return session.get("admin_logged_in", False)

# =========================================================
# ARTICLES CRUD
# =========================================================
@crud_bp.route("/articles/create", methods=["POST"])
def create_article():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip().lower()

        if not title or not content or not category:
            flash("Tous les champs de l'article sont obligatoires.", "danger")
            return redirect(url_for("admin.admin_new_article"))

        if category not in ["femme", "enfant", "famille"]:
            flash("Catégorie invalide pour l'article.", "danger")
            return redirect(url_for("admin.admin_new_article"))

        article = Article(title=title, content=content, category=category)
        db.session.add(article)
        db.session.commit()

        flash("Article ajouté avec succès.", "success")
        return redirect(url_for("admin.admin_articles"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de l'ajout de l'article : {str(e)}", "danger")
        return redirect(url_for("admin.admin_new_article"))

@crud_bp.route("/articles/<int:article_id>/update", methods=["POST"])
def update_article(article_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        article = Article.query.get_or_404(article_id)
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip().lower()

        if not title or not content or not category:
            flash("Tous les champs de l'article sont obligatoires.", "danger")
            return redirect(url_for("admin.admin_articles"))

        if category not in ["femme", "enfant", "famille"]:
            flash("Catégorie invalide pour l'article.", "danger")
            return redirect(url_for("admin.admin_articles"))

        article.title = title
        article.content = content
        article.category = category
        db.session.commit()

        flash("Article modifié avec succès.", "success")
        return redirect(url_for("admin.admin_articles"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la modification de l'article : {str(e)}", "danger")
        return redirect(url_for("admin.admin_articles"))

@crud_bp.route("/articles/<int:article_id>/delete", methods=["POST"])
def delete_article(article_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()

        flash("Article supprimé avec succès.", "success")
        return redirect(url_for("admin.admin_articles"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression de l'article : {str(e)}", "danger")
        return redirect(url_for("admin.admin_articles"))

# =========================================================
# GUIDES CRUD
# =========================================================
@crud_bp.route("/guides/create", methods=["POST"])
def create_guide():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        case_type = request.form.get("case_type", "").strip().lower()

        if not title or not content or not case_type:
            flash("Tous les champs du guide sont obligatoires.", "danger")
            return redirect(url_for("admin.admin_new_guide"))

        if case_type not in ["violence", "harcelement", "abus", "litiges"]:
            flash("Type de cas invalide pour le guide.", "danger")
            return redirect(url_for("admin.admin_new_guide"))

        guide = Guide(title=title, content=content, case_type=case_type)
        db.session.add(guide)
        db.session.commit()

        flash("Guide ajouté avec succès.", "success")
        return redirect(url_for("admin.admin_guides"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de l'ajout du guide : {str(e)}", "danger")
        return redirect(url_for("admin.admin_new_guide"))

@crud_bp.route("/guides/<int:guide_id>/update", methods=["POST"])
def update_guide(guide_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        guide = Guide.query.get_or_404(guide_id)
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        case_type = request.form.get("case_type", "").strip().lower()

        if not title or not content or not case_type:
            flash("Tous les champs du guide sont obligatoires.", "danger")
            return redirect(url_for("admin.admin_guides"))

        if case_type not in ["violence", "harcelement", "abus", "litiges"]:
            flash("Type de cas invalide pour le guide.", "danger")
            return redirect(url_for("admin.admin_guides"))

        guide.title = title
        guide.content = content
        guide.case_type = case_type
        db.session.commit()

        flash("Guide modifié avec succès.", "success")
        return redirect(url_for("admin.admin_guides"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la modification du guide : {str(e)}", "danger")
        return redirect(url_for("admin.admin_guides"))

@crud_bp.route("/guides/<int:guide_id>/delete", methods=["POST"])
def delete_guide(guide_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        guide = Guide.query.get_or_404(guide_id)
        db.session.delete(guide)
        db.session.commit()

        flash("Guide supprimé avec succès.", "success")
        return redirect(url_for("admin.admin_guides"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression du guide : {str(e)}", "danger")
        return redirect(url_for("admin.admin_guides"))

# =========================================================
# CONTACTS CRUD
# =========================================================
@crud_bp.route("/contacts/create", methods=["POST"])
def create_contact():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        specialty = request.form.get("specialty", "").strip()

        if not name or not role or not phone:
            flash("Nom, rôle et téléphone sont obligatoires.", "danger")
            return redirect(url_for("admin.admin_new_contact"))

        contact = Contact(
            name=name,
            role=role,
            email=email if email else None,
            phone=phone,
            address=address if address else None,
            specialty=specialty if specialty else None
        )
        db.session.add(contact)
        db.session.commit()

        flash("Contact ajouté avec succès.", "success")
        return redirect(url_for("admin.admin_contacts"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de l'ajout du contact : {str(e)}", "danger")
        return redirect(url_for("admin.admin_new_contact"))

@crud_bp.route("/contacts/<int:contact_id>/update", methods=["POST"])
def update_contact(contact_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        contact = Contact.query.get_or_404(contact_id)
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        specialty = request.form.get("specialty", "").strip()

        if not name or not role or not phone:
            flash("Nom, rôle et téléphone sont obligatoires.", "danger")
            return redirect(url_for("admin.admin_contacts"))

        contact.name = name
        contact.role = role
        contact.email = email if email else None
        contact.phone = phone
        contact.address = address if address else None
        contact.specialty = specialty if specialty else None
        db.session.commit()

        flash("Contact modifié avec succès.", "success")
        return redirect(url_for("admin.admin_contacts"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la modification du contact : {str(e)}", "danger")
        return redirect(url_for("admin.admin_contacts"))

@crud_bp.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def delete_contact(contact_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))
    try:
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()

        flash("Contact supprimé avec succès.", "success")
        return redirect(url_for("admin.admin_contacts"))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression du contact : {str(e)}", "danger")
        return redirect(url_for("admin.admin_contacts"))