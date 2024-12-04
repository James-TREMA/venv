from flask import Flask, jsonify, request, render_template
from peewee import *
from Model.departement import Departement
from Model.villes_france_free import VillesFranceFree
from Model.MOCK_DATA import MockData
from Model.base import database

# Configuration Flask
app = Flask(__name__)

# Middleware pour gérer les connexions Peewee
@app.before_request
def before_request():
    if database.is_closed():
        database.connect()

@app.teardown_request
def teardown_request(exc):
    if not database.is_closed():
        database.close()

# Centralisation des erreurs
def handle_error(message, status_code=404):
    return jsonify({"error": message}), status_code

# Routes API

@app.route('/')
def home():
    return render_template('index.html')

# Route pour afficher tous les départements
@app.route('/departements', methods=['GET'])
def display_departements():
    departments = Departement.select()
    return render_template('departements.html', departments=departments)

@app.route('/villes', methods=['GET'])
def display_villes():
    villes = VillesFranceFree.select()
    return render_template('villes.html', villes=villes)

@app.route('/mock_data', methods=['GET'])
def display_mock_data():
    mock_data = MockData.select()
    return render_template('mock_data.html', mock_data=mock_data)


# Route pour récupérer un département par ID
@app.route('/api/departements/<int:departement_id>', methods=['GET'])
def get_departement_by_id(departement_id):
    try:
        departement = Departement.get(Departement.departement_id == departement_id)
        return jsonify({
            "departement_id": departement.departement_id,
            "departement_code": departement.departement_code,
            "departement_nom": departement.departement_nom,
            "departement_nom_uppercase": departement.departement_nom_uppercase,
            "departement_slug": departement.departement_slug,
            "departement_nom_soundex": departement.departement_nom_soundex,
        })
    except Departement.DoesNotExist:
        return handle_error(f"Département avec l'ID {departement_id} non trouvé")

# Route pour récupérer un département par code
@app.route('/api/departements/code/<string:departement_code>', methods=['GET'])
def get_departement_by_code(departement_code):
    try:
        departement = Departement.get(Departement.departement_code == departement_code)
        return jsonify({
            "departement_id": departement.departement_id,
            "departement_code": departement.departement_code,
            "departement_nom": departement.departement_nom,
            "departement_nom_uppercase": departement.departement_nom_uppercase,
            "departement_slug": departement.departement_slug,
            "departement_nom_soundex": departement.departement_nom_soundex,
        })
    except Departement.DoesNotExist:
        return handle_error(f"Département avec le code {departement_code} non trouvé")

# Route pour récupérer les villes d’un département
@app.route('/api/villes/departement/<string:departement_code>', methods=['GET'])
def get_villes_by_departement(departement_code):
    villes = VillesFranceFree.select().where(VillesFranceFree.ville_departement == departement_code)
    return jsonify([{
        "ville_id": ville.ville_id,
        "ville_departement": ville.ville_departement,
        "ville_slug": ville.ville_slug,
        "ville_nom_simple": ville.ville_nom_simple,
        "ville_nom_reel": ville.ville_nom_reel,
        "ville_code_postal": ville.ville_code_postal,
        "ville_population": ville.ville_population_2010,
    } for ville in villes]) if villes else handle_error("Aucune ville trouvée pour ce département")

# Route pour récupérer les données Mock
@app.route('/api/mock_data', methods=['GET'])
def get_mock_data():
    data = MockData.select()
    return jsonify([{
        "id": record.id,
        "first_name": record.first_name,
        "last_name": record.last_name,
        "email": record.email,
        "gender": record.gender,
        "ip_address": record.ip_address,
    } for record in data])

# Route pour ajouter un enregistrement Mock
@app.route('/api/mock_data', methods=['POST'])
def add_mock_data():
    data = request.get_json()
    new_record = MockData.create(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        gender=data.get('gender'),
        ip_address=data.get('ip_address'),
    )
    return jsonify({"message": "Enregistrement ajouté avec succès", "id": new_record.id}), 201

# Route pour mettre à jour un enregistrement Mock
@app.route('/api/mock_data/<int:record_id>', methods=['PUT'])
def update_mock_data(record_id):
    try:
        data = request.get_json()
        record = MockData.get(MockData.id == record_id)
        record.first_name = data.get('first_name')
        record.last_name = data.get('last_name')
        record.email = data.get('email')
        record.gender = data.get('gender')
        record.ip_address = data.get('ip_address')
        record.save()
        return jsonify({"message": "Enregistrement mis à jour avec succès"}), 200
    except MockData.DoesNotExist:
        return handle_error(f"Enregistrement avec l'ID {record_id} non trouvé")

# Route pour supprimer un enregistrement Mock
@app.route('/api/mock_data/<int:record_id>', methods=['DELETE'])
def delete_mock_data(record_id):
    try:
        record = MockData.get(MockData.id == record_id)
        record.delete_instance()
        return jsonify({"message": "Enregistrement supprimé avec succès"}), 200
    except MockData.DoesNotExist:
        return handle_error(f"Enregistrement avec l'ID {record_id} non trouvé")

if __name__ == '__main__':
    app.run(debug=True)
