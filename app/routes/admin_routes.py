from flask import Blueprint, request, jsonify
from app.models import db, Litige, Avocat, RdvAvocat

admin_bp = Blueprint('admin', __name__)

# Lister tous les litiges
@admin_bp.route('/api/admin/litiges', methods=['GET'])
def admin_litiges():
    litiges = Litige.query.all()
    return jsonify([{
        'id': l.id,
        'user_id': l.user_id,
        'title': l.title,
        'description': l.description,
        'status': l.status,
        'created_at': l.created_at
    } for l in litiges])

# Gestion des avocats
@admin_bp.route('/api/admin/avocats', methods=['POST', 'PUT', 'DELETE'])
def manage_avocats():
    data = request.get_json()
    if request.method == 'POST':
        avocat = Avocat(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            speciality=data.get('speciality'),
            available=data.get('available', True)
        )
        db.session.add(avocat)
        db.session.commit()
        return jsonify({'message': 'Avocat ajouté', 'id': avocat.id}), 201

    if request.method == 'PUT':
        avocat = Avocat.query.get(data['id'])
        if not avocat:
            return jsonify({'message': 'Avocat non trouvé'}), 404
        for key, value in data.items():
            if hasattr(avocat, key):
                setattr(avocat, key, value)
        db.session.commit()
        return jsonify({'message': 'Avocat mis à jour'})

    if request.method == 'DELETE':
        avocat = Avocat.query.get(data['id'])
        if not avocat:
            return jsonify({'message': 'Avocat non trouvé'}), 404
        db.session.delete(avocat)
        db.session.commit()
        return jsonify({'message': 'Avocat supprimé'})

# Liste des rendez-vous pour gestion admin
@admin_bp.route('/api/admin/rdv', methods=['GET'])
def admin_rdvs():
    rdvs = RdvAvocat.query.all()
    return jsonify([{
        'id': r.id,
        'user_id': r.user_id,
        'avocat_id': r.avocat_id,
        'litige_id': r.litige_id,
        'date_rdv': r.date_rdv,
        'status': r.status
    } for r in rdvs])
