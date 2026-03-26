from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Article, Guide, Contact, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================================================
# CONFIG ADMIN SIMPLE (EN DUR POUR V1)
# =========================================================
ADMIN_USERNAME = "Ellesaidmin"
ADMIN_PASSWORD = "elleaid@2026"


def is_admin_logged_in():
    return session.get("admin_logged_in", False)


# =========================================================
# LOGIN / LOGOUT ADMIN
# =========================================================
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            flash("Connexion réussie.", "success")
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
            return redirect(url_for("admin.admin_login"))

    return render_template("admin/login.html")


@admin_bp.route("/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("Déconnexion réussie.", "success")
    return redirect(url_for("admin.admin_login"))


# =========================================================
# DASHBOARD
# =========================================================
@admin_bp.route("/")
def admin_dashboard():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    article_count = Article.query.count()
    guide_count = Guide.query.count()
    contact_count = Contact.query.count()
    user_count = User.query.count()

    return render_template(
        "admin/dashboard.html",
        article_count=article_count,
        guide_count=guide_count,
        contact_count=contact_count,
        user_count=user_count
    )


# =========================================================
# ARTICLES PAGES
# =========================================================
@admin_bp.route("/articles")
def admin_articles():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("admin/articles_list.html", articles=articles)


@admin_bp.route("/articles/new")
def admin_new_article():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    return render_template("admin/article_form.html")


@admin_bp.route("/articles/<int:article_id>/edit")
def admin_edit_article(article_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    article = Article.query.get_or_404(article_id)
    return render_template("admin/article_form.html", article=article)


# =========================================================
# GUIDES PAGES
# =========================================================
@admin_bp.route("/guides")
def admin_guides():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    guides = Guide.query.order_by(Guide.created_at.desc()).all()
    return render_template("admin/guides_list.html", guides=guides)


@admin_bp.route("/guides/new")
def admin_new_guide():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    return render_template("admin/guide_form.html")


@admin_bp.route("/guides/<int:guide_id>/edit")
def admin_edit_guide(guide_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    guide = Guide.query.get_or_404(guide_id)
    return render_template("admin/guide_form.html", guide=guide)


# =========================================================
# CONTACTS PAGES
# =========================================================
@admin_bp.route("/contacts")
def admin_contacts():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template("admin/contacts_list.html", contacts=contacts)


@admin_bp.route("/contacts/new")
def admin_new_contact():
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    return render_template("admin/contact_form.html")


@admin_bp.route("/contacts/<int:contact_id>/edit")
def admin_edit_contact(contact_id):
    if not is_admin_logged_in():
        return redirect(url_for("admin.admin_login"))

    contact = Contact.query.get_or_404(contact_id)
    return render_template("admin/contact_form.html", contact=contact)