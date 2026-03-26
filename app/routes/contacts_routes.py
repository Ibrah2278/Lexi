from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Contact

contacts_bp = Blueprint("contacts", __name__, url_prefix="/api/contacts")


# =========================================================
# GET ALL CONTACTS
# GET /api/contacts
# Query params:
# - role=Avocat|ONG|Association
# - specialty=...
# - q=motclé
# =========================================================
@contacts_bp.route("", methods=["GET"])
def get_contacts():
    try:
        role = request.args.get("role", "").strip()
        specialty = request.args.get("specialty", "").strip().lower()
        q = request.args.get("q", "").strip().lower()

        query = Contact.query

        if role:
            query = query.filter(Contact.role.ilike(f"%{role}%"))

        if specialty:
            query = query.filter(Contact.specialty.ilike(f"%{specialty}%"))

        if q:
            query = query.filter(
                (Contact.name.ilike(f"%{q}%")) |
                (Contact.role.ilike(f"%{q}%")) |
                (Contact.specialty.ilike(f"%{q}%")) |
                (Contact.address.ilike(f"%{q}%"))
            )

        contacts = query.order_by(Contact.created_at.desc()).all()

        return jsonify({
            "success": True,
            "count": len(contacts),
            "contacts": [contact.to_dict() for contact in contacts]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération des contacts",
            "error": str(e)
        }), 500


# =========================================================
# GET CONTACT BY ID
# GET /api/contacts/<id>
# =========================================================
@contacts_bp.route("/<int:contact_id>", methods=["GET"])
def get_contact_by_id(contact_id):
    try:
        contact = Contact.query.get(contact_id)

        if not contact:
            return jsonify({
                "success": False,
                "message": "Contact introuvable"
            }), 404

        return jsonify({
            "success": True,
            "contact": contact.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erreur lors de la récupération du contact",
            "error": str(e)
        }), 500


# =========================================================
# CREATE CONTACT
# POST /api/contacts
# =========================================================
@contacts_bp.route("", methods=["POST"])
def create_contact():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        name = data.get("name", "").strip()
        role = data.get("role", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()
        specialty = data.get("specialty", "").strip()

        if not name or not role:
            return jsonify({
                "success": False,
                "message": "Nom et rôle sont obligatoires"
            }), 400

        new_contact = Contact(
            name=name,
            role=role,
            email=email if email else None,
            phone=phone if phone else None,
            address=address if address else None,
            specialty=specialty if specialty else None
        )

        db.session.add(new_contact)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Contact créé avec succès",
            "contact": new_contact.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la création du contact",
            "error": str(e)
        }), 500


# =========================================================
# UPDATE CONTACT
# PUT /api/contacts/<id>
# =========================================================
@contacts_bp.route("/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)

        if not contact:
            return jsonify({
                "success": False,
                "message": "Contact introuvable"
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Aucune donnée reçue"
            }), 400

        if "name" in data:
            contact.name = data.get("name", "").strip()

        if "role" in data:
            contact.role = data.get("role", "").strip()

        if "email" in data:
            email = data.get("email", "").strip()
            contact.email = email if email else None

        if "phone" in data:
            phone = data.get("phone", "").strip()
            contact.phone = phone if phone else None

        if "address" in data:
            address = data.get("address", "").strip()
            contact.address = address if address else None

        if "specialty" in data:
            specialty = data.get("specialty", "").strip()
            contact.specialty = specialty if specialty else None

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Contact mis à jour avec succès",
            "contact": contact.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la mise à jour du contact",
            "error": str(e)
        }), 500


# =========================================================
# DELETE CONTACT
# DELETE /api/contacts/<id>
# =========================================================
@contacts_bp.route("/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)

        if not contact:
            return jsonify({
                "success": False,
                "message": "Contact introuvable"
            }), 404

        db.session.delete(contact)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Contact supprimé avec succès"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erreur lors de la suppression du contact",
            "error": str(e)
        }), 500