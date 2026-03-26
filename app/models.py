from datetime import datetime
from .extensions import db, bcrypt


# =========================================================
# USER
# =========================================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    favorites = db.relationship("Favorite", backref="user", lazy=True, cascade="all, delete-orphan")
    search_history = db.relationship("SearchHistory", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<User {self.email}>"


# =========================================================
# ARTICLE
# =========================================================
class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.Enum("femme", "enfant", "famille", name="article_categories"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_content=True):
        data = {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if include_content:
            data["content"] = self.content
        return data

    def __repr__(self):
        return f"<Article {self.title}>"


# =========================================================
# GUIDE
# =========================================================
class Guide(db.Model):
    __tablename__ = "guides"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    case_type = db.Column(
        db.Enum("violence", "harcelement", "abus", "litiges", name="guide_case_types"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_content=True):
        data = {
            "id": self.id,
            "title": self.title,
            "case_type": self.case_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        if include_content:
            data["content"] = self.content
        return data

    def __repr__(self):
        return f"<Guide {self.title}>"


# =========================================================
# CONTACT
# =========================================================
class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=False)  # Avocat / ONG / Association
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    specialty = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "specialty": self.specialty,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Contact {self.name}>"


# =========================================================
# FAVORITE
# =========================================================
class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(
        db.Enum("article", "guide", "contact", name="favorite_types"),
        nullable=False
    )
    item_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "item_id": self.item_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Favorite {self.type}:{self.item_id}>"


# =========================================================
# SEARCH HISTORY
# =========================================================
class SearchHistory(db.Model):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    query = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query": self.query,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<SearchHistory {self.query}>"