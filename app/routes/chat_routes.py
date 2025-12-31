from flask import Blueprint, request, jsonify
from app.models import db, ChatHistory, Litige
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

# Envoyer message et recevoir réponse (simulée pour le moment)
@chat_bp.route('/api/chat/send', methods=['POST'])
def chat_send():
    data = request.get_json()
    user_id = data['user_id']
    litige_id = data.get('litige_id')
    message = data['message']

    # Enregistrer message utilisateur
    chat_user = ChatHistory(user_id=user_id, litige_id=litige_id, message=message, sender='user')
    db.session.add(chat_user)

    # Génération réponse bot (à remplacer par logique IA plus tard)
    bot_response = f"Réponse générique à votre message: {message}"
    chat_bot = ChatHistory(user_id=user_id, litige_id=litige_id, message=bot_response, sender='bot')
    db.session.add(chat_bot)
    db.session.commit()

    return jsonify({'bot_message': bot_response})

# Historique des conversations
@chat_bp.route('/api/chat/history/<int:user_id>', methods=['GET'])
def chat_history(user_id):
    chats = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.created_at).all()
    return jsonify([{
        'id': c.id,
        'litige_id': c.litige_id,
        'message': c.message,
        'sender': c.sender,
        'created_at': c.created_at
    } for c in chats])
