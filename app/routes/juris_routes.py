from flask import Blueprint, request, jsonify
from app.models import db, ArticleDroit, Avocat

juris_bp = Blueprint('juris', __name__)

# Articles de loi
@juris_bp.route('/api/articles', methods=['GET'])
def get_articles():
    category = request.args.get('category')
    keyword = request.args.get('keyword')
    query = ArticleDroit.query
    if category:
        query = query.filter(ArticleDroit.category.ilike(f"%{category}%"))
    if keyword:
        query = query.filter(ArticleDroit.title.ilike(f"%{keyword}%") | ArticleDroit.content.ilike(f"%{keyword}%"))
    articles = query.all()
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'category': a.category
    } for a in articles])

# Liste des avocats disponibles (option filtre spécialité)
@juris_bp.route('/api/avocats', methods=['GET'])
def get_avocats():
    speciality = request.args.get('speciality')
    query = Avocat.query.filter_by(available=True)
    if speciality:
        query = query.filter(Avocat.speciality.ilike(f"%{speciality}%"))
    avocats = query.all()
    return jsonify([{
        'id': a.id,
        'first_name': a.first_name,
        'last_name': a.last_name,
        'email': a.email,
        'phone': a.phone,
        'speciality': a.speciality,
        'rating': a.rating
    } for a in avocats])
