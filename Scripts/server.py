from flask import Flask, jsonify, request, render_template
from peewee import *
from Model.departement import Departement
from Model.villes_france_free import VillesFranceFree
from Model.MOCK_DATA import MockData

# Configuration Flask
app = Flask(__name__)

# Connexion Peewee
database = MySQLDatabase(
    'francedb',
    user='root',
    password='root',
    host='localhost',
    charset='utf8mb4'
)

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

@app.route('/departements', methods=['GET'])
def display_departements():
    departments = Departement.select()
    return render_template('departements.html', departments=departments)

@app.route('/api/departements/<int:departement_id>', methods=['GET'])
def get_departement_by_id(departement_id):
    try:
        departement = Departement.get(Departement.departement_id == departement_id)
        return jsonify({
            "departement_id": departement.departement_id,
            "departement_code": departement.departement_code,
            "departement_name": departement.departement_name,
        })
    except Departement.DoesNotExist:
        return handle_error(f"Département avec l'ID {departement_id} non trouvé")

@app.route('/api/departements/code/<string:departement_code>', methods=['GET'])
def get_departement_by_code(departement_code):
    try:
        departement = Departement.get(Departement.departement_code == departement_code)
        return jsonify({
            "departement_id": departement.departement_id,
            "departement_code": departement.departement_code,
            "departement_name": departement.departement_name,
        })
    except Departement.DoesNotExist:
        return handle_error(f"Département avec le code {departement_code} non trouvé")

@app.route('/api/villes/departement/<string:departement_code>', methods=['GET'])
def get_villes_by_departement(departement_code):
    villes = VillesFranceFree.select().where(VillesFranceFree.ville_departement == departement_code)
    return jsonify([{
        "ville_id": ville.ville_id,
        "ville_departement": ville.ville_departement,
        "ville_nom": ville.ville_nom,
        "ville_code_postal": ville.ville_code_postal,
        "ville_population": ville.ville_population,
    } for ville in villes]) if villes else handle_error("Aucune ville trouvée pour ce département")

@app.route('/api/villes/nom/<string:ville_nom>', methods=['GET'])
def get_villes_by_nom(ville_nom):
    villes = VillesFranceFree.select().where(VillesFranceFree.ville_nom == ville_nom)
    return jsonify([{
        "ville_id": ville.ville_id,
        "ville_departement": ville.ville_departement,
        "ville_nom": ville.ville_nom,
        "ville_code_postal": ville.ville_code_postal,
        "ville_population": ville.ville_population,
    } for ville in villes]) if villes else handle_error("Aucune ville trouvée")

@app.route('/api/villes/code_postal/<string:code_postal>', methods=['GET'])
def get_villes_by_code_postal(code_postal):
    villes = VillesFranceFree.select().where(VillesFranceFree.ville_code_postal == code_postal)
    return jsonify([{
        "ville_id": ville.ville_id,
        "ville_departement": ville.ville_departement,
        "ville_nom": ville.ville_nom,
        "ville_code_postal": ville.ville_code_postal,
        "ville_population": ville.ville_population,
    } for ville in villes]) if villes else handle_error("Aucune ville trouvée")

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

@app.route('/api/mock_data/<int:record_id>', methods=['GET'])
def get_mock_data_by_id(record_id):
    try:
        record = MockData.get(MockData.id == record_id)
        return jsonify({
            "id": record.id,
            "first_name": record.first_name,
            "last_name": record.last_name,
            "email": record.email,
            "gender": record.gender,
            "ip_address": record.ip_address,
        })
    except MockData.DoesNotExist:
        return handle_error(f"Enregistrement avec l'ID {record_id} non trouvé")

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