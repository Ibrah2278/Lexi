from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    litiges = db.relationship('Litige', backref='user', cascade="all, delete-orphan")
    chat_history = db.relationship('ChatHistory', backref='user', cascade="all, delete-orphan")
    rdv_avocat = db.relationship('RdvAvocat', backref='user', cascade="all, delete-orphan")


class Litige(db.Model):
    __tablename__ = 'litiges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('en cours', 'résolu', 'en attente'), default='en cours')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chat_history = db.relationship('ChatHistory', backref='litige', cascade="all, delete-orphan")
    rdv_avocat = db.relationship('RdvAvocat', backref='litige', cascade="all, delete-orphan")


class ArticleDroit(db.Model):
    __tablename__ = 'articles_droit'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    litige_id = db.Column(db.Integer, db.ForeignKey('litiges.id', ondelete='SET NULL'))
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.Enum('user','bot'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Avocat(db.Model):
    __tablename__ = 'avocats'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    speciality = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0)
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    rdv_avocat = db.relationship('RdvAvocat', backref='avocat', cascade="all, delete-orphan")


class RdvAvocat(db.Model):
    __tablename__ = 'rdv_avocat'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    avocat_id = db.Column(db.Integer, db.ForeignKey('avocats.id', ondelete='CASCADE'), nullable=False)
    litige_id = db.Column(db.Integer, db.ForeignKey('litiges.id', ondelete='CASCADE'), nullable=False)
    date_rdv = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('planifié','réalisé','annulé'), default='planifié')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
