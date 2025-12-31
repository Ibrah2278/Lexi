from flask import Blueprint, request, jsonify
from app.models import db, User, Litige, RdvAvocat
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_bp = Blueprint('user', __name__)

# Inscription
@user_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        password_hash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur créé avec succès'}), 201

# Login
@user_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Connexion réussie', 'user_id': user.id})
    return jsonify({'message': 'Email ou mot de passe incorrect'}), 401

# Liste litiges utilisateur
@user_bp.route('/api/litiges', methods=['GET'])
def get_litiges():
    user_id = request.args.get('user_id')
    litiges = Litige.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': l.id,
        'title': l.title,
        'description': l.description,
        'status': l.status,
        'created_at': l.created_at
    } for l in litiges])

# Création nouveau litige
@user_bp.route('/api/litiges', methods=['POST'])
def create_litige():
    data = request.get_json()
    new_litige = Litige(
        user_id=data['user_id'],
        title=data['title'],
        description=data.get('description')
    )
    db.session.add(new_litige)
    db.session.commit()
    return jsonify({'message': 'Litige créé avec succès', 'id': new_litige.id}), 201

# Créer rendez-vous
@user_bp.route('/api/rdv', methods=['POST'])
def create_rdv():
    data = request.get_json()
    rdv = RdvAvocat(
        user_id=data['user_id'],
        avocat_id=data['avocat_id'],
        litige_id=data['litige_id'],
        date_rdv=datetime.fromisoformat(data['date_rdv'])
    )
    db.session.add(rdv)
    db.session.commit()
    return jsonify({'message': 'Rendez-vous créé', 'id': rdv.id}), 201

# Récupérer rendez-vous utilisateur
@user_bp.route('/api/rdv/<int:user_id>', methods=['GET'])
def get_rdv(user_id):
    rdvs = RdvAvocat.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': r.id,
        'avocat_id': r.avocat_id,
        'litige_id': r.litige_id,
        'date_rdv': r.date_rdv,
        'status': r.status
    } for r in rdvs])
