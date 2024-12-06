from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from Model.users import User
from peewee import IntegrityError

# Création du blueprint pour les routes utilisateurs
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# === Création d'un utilisateur ===
@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Route pour créer un nouvel utilisateur.
    """
    try:
        # Récupération des données envoyées par le client
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validation des données
        if not username or not email or not password:
            return jsonify({"error": "Tous les champs sont obligatoires (username, email, password)."}), 400

        # Création de l'utilisateur
        hashed_password = generate_password_hash(password)
        new_user = User.create(
            username=username,
            email=email,
            password=hashed_password
        )
        return jsonify({
            "message": "Utilisateur créé avec succès.",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at
            }
        }), 201

    except IntegrityError as e:
        # Gérer les erreurs de doublon
        return jsonify({"error": "Le nom d'utilisateur ou l'email existe déjà."}), 409

    except Exception as e:
        # Gestion des erreurs générales
        return jsonify({"error": "Une erreur est survenue lors de la création de l'utilisateur."}), 500
