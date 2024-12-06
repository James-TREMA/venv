from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from Model.MOCK_DATA import MockData  # Exemple d'utilisation de la base actuelle
from peewee import IntegrityError

# Création du blueprint pour les routes utilisateurs
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# === Création d'un utilisateur ===
@users_bp.route('/', methods=['POST'])
def create_user():
    # Ajoute un nouvel utilisateur
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        gender = data.get('gender')
        ip_address = data.get('ip_address')

        # Validation des données
        if not all([first_name, last_name, email, gender, ip_address]):
            return jsonify({"error": "Tous les champs sont obligatoires."}), 400

        # Création de l'utilisateur
        new_user = MockData.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            ip_address=ip_address
        )

        return jsonify({
            "message": "Utilisateur créé avec succès.",
            "user": {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "gender": new_user.gender,
                "ip_address": new_user.ip_address
            }
        }), 201

    except IntegrityError:
        return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 409

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création : {str(e)}"}), 500

# === Obtenir tous les utilisateurs ===
@users_bp.route('/', methods=['GET'])
def get_all_users():
    # Retourne tous les utilisateurs
    users = MockData.select()
    return jsonify([{
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "gender": user.gender,
        "ip_address": user.ip_address
    } for user in users])

# === Supprimer un utilisateur par ID ===
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Supprime un utilisateur par ID
    try:
        user = MockData.get(MockData.id == user_id)
        user.delete_instance()
        return jsonify({"message": "Utilisateur supprimé avec succès."}), 200
    except MockData.DoesNotExist:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

# === Mise à jour partielle d'un utilisateur ===
@users_bp.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    # Met à jour partiellement les informations d'un utilisateur
    try:
        user = MockData.get(MockData.id == user_id)
        data = request.get_json()

        # Mise à jour uniquement des champs fournis
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'gender' in data:
            user.gender = data['gender']
        if 'ip_address' in data:
            user.ip_address = data['ip_address']

        # Enregistrement des modifications
        user.save()
        return jsonify({
            "message": "Utilisateur mis à jour avec succès.",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "gender": user.gender,
                "ip_address": user.ip_address
            }
        }), 200

    except MockData.DoesNotExist:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    except IntegrityError:
        return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 409

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour : {str(e)}"}), 500
