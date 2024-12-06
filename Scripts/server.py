from flask import Flask, jsonify, request, render_template
from peewee import *
from Model.departement import Departement
from Model.villes_france_free import VillesFranceFree
from Model.MOCK_DATA import MockData
from Model.base import database

# === Configuration de l'application Flask ===
app = Flask(__name__)

# === Gestion des connexions Peewee ===
@app.before_request
def before_request():
    # Ouvre une connexion à la base de données si elle est fermée
    if database.is_closed():
        database.connect()

@app.teardown_request
def teardown_request(exc):
    # Ferme la connexion à la base de données après chaque requête
    if not database.is_closed():
        database.close()

# === Gestion centralisée des erreurs ===
def handle_error(message, status_code=404):
    # Retourne une réponse JSON pour une erreur
    return jsonify({"error": message}), status_code

# === Routes Web ===

@app.route('/')
def home():
    # Affiche la page d'accueil
    return render_template('index.html')

@app.route('/departements', methods=['GET'])
def display_departements():
    # Affiche la liste des départements avec pagination
    page = int(request.args.get('page', 1))  # Page actuelle
    per_page = 50  # Nombre d'éléments par page
    offset = (page - 1) * per_page  # Calcul de l'offset

    # Récupération des données
    query = Departement.select()
    departments = query.limit(per_page).offset(offset)

    # Calcul du nombre total de pages
    total_departments = query.count()
    total_pages = (total_departments // per_page) + (1 if total_departments % per_page > 0 else 0)

    # Rendu du template
    return render_template(
        'departements.html',
        departments=departments,
        page=page,
        total_pages=total_pages,
        max=max,  # Fonction max pour le template
        min=min   # Fonction min pour le template
    )

@app.route('/villes', methods=['GET'])
def display_villes():
    # Affiche les villes avec recherche et pagination
    search_query = request.args.get('search', '').strip()  # Recherche (facultative)
    page = int(request.args.get('page', 1))  # Page actuelle
    per_page = 50  # Nombre d'éléments par page
    offset = (page - 1) * per_page  # Calcul de l'offset

    # Filtrage des villes par recherche
    query = VillesFranceFree.select()
    if search_query:
        query = query.where(VillesFranceFree.ville_nom_reel.contains(search_query))

    villes = query.limit(per_page).offset(offset)

    # Calcul du nombre total de pages
    total_villes = query.count()
    total_pages = (total_villes // per_page) + (1 if total_villes % per_page > 0 else 0)

    # Rendu du template
    return render_template(
        'villes.html',
        villes=villes,
        page=page,
        total_pages=total_pages,
        search_query=search_query,
        max=max,
        min=min
    )

@app.route('/mock_data', methods=['GET'])
def display_mock_data():
    # Affiche les données Mock avec pagination
    page = int(request.args.get('page', 1))  # Page actuelle
    per_page = 50  # Nombre d'éléments par page
    offset = (page - 1) * per_page  # Calcul de l'offset

    # Récupération des données
    query = MockData.select()
    mock_data = query.limit(per_page).offset(offset)

    # Calcul du nombre total de pages
    total_mock_data = query.count()
    total_pages = (total_mock_data // per_page) + (1 if total_mock_data % per_page > 0 else 0)

    # Rendu du template
    return render_template(
        'mock_data.html',
        mock_data=mock_data,
        page=page,
        total_pages=total_pages,
        max=max,
        min=min
    )

# === Routes API ===

@app.route('/api/departements/<int:departement_id>', methods=['GET'])
def get_departement_by_id(departement_id):
    # Retourne les détails d'un département par son ID
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

@app.route('/api/departements/code/<string:departement_code>', methods=['GET'])
def get_departement_by_code(departement_code):
    # Retourne les détails d'un département par son code
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

@app.route('/api/villes/departement/<string:departement_code>', methods=['GET'])
def get_villes_by_departement(departement_code):
    # Retourne les villes associées à un département
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

@app.route('/api/mock_data', methods=['GET'])
def get_mock_data():
    # Retourne toutes les données Mock au format JSON
    data = MockData.select()
    return jsonify([{
        "id": record.id,
        "first_name": record.first_name,
        "last_name": record.last_name,
        "email": record.email,
        "gender": record.gender,
        "ip_address": record.ip_address,
    } for record in data])

@app.route('/api/mock_data', methods=['POST'])
def add_mock_data():
    # Ajoute un nouvel enregistrement Mock
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
    # Met à jour un enregistrement Mock existant
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
    # Supprime un enregistrement Mock par son ID
    try:
        record = MockData.get(MockData.id == record_id)
        record.delete_instance()
        return jsonify({"message": "Enregistrement supprimé avec succès"}), 200
    except MockData.DoesNotExist:
        return handle_error(f"Enregistrement avec l'ID {record_id} non trouvé")

# === Lancement de l'application ===
if __name__ == '__main__':
    app.run(debug=True)
