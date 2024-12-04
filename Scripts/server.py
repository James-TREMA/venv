from flask import Flask, jsonify, request, render_template
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

# Configuration globale pour la base de données
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'francedb',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
}

# Gestionnaire de connexion à la base de données
class DatabaseConnection:
    def __enter__(self):
        self.connection = pymysql.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

# Centralisation des erreurs
def handle_error(message, status_code=404):
    return jsonify({"error": message}), status_code

# Routes API
@app.route('/api/departements', methods=['GET'])
def get_departements():
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM departement")
        result = cursor.fetchall()
    return jsonify(result) if result else handle_error("Aucun département trouvé")

@app.route('/api/departements/<int:departement_id>', methods=['GET'])
def get_departement_by_id(departement_id):
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM departement WHERE departement_id = %s", (departement_id,))
        result = cursor.fetchone()
    return jsonify(result) if result else handle_error(f"Département avec l'ID {departement_id} non trouvé")

@app.route('/api/departements/code/<string:departement_code>', methods=['GET'])
def get_departement_by_code(departement_code):
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM departement WHERE departement_code = %s", (departement_code,))
        result = cursor.fetchone()
    return jsonify(result) if result else handle_error(f"Département avec le code {departement_code} non trouvé")

@app.route('/api/villes/departement/<string:departement_code>', methods=['GET'])
def get_villes_by_departement(departement_code):
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM villes_france_free WHERE ville_departement = %s", (departement_code,))
        result = cursor.fetchall()
    return jsonify(result) if result else handle_error("Aucune ville trouvée pour ce département")

@app.route('/api/villes/nom/<string:ville_nom>', methods=['GET'])
def get_villes_by_nom(ville_nom):
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM villes_france_free WHERE ville_nom = %s", (ville_nom,))
        result = cursor.fetchall()
    return jsonify(result) if result else handle_error("Aucune ville trouvée")

@app.route('/api/villes/code_postal/<string:code_postal>', methods=['GET'])
def get_villes_by_code_postal(code_postal):
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM villes_france_free WHERE ville_code_postal = %s", (code_postal,))
        result = cursor.fetchall()
    return jsonify(result) if result else handle_error("Aucune ville trouvée")

@app.route('/api/villes/population/<int:annee>/<int:population>', methods=['GET'])
def get_villes_by_population(annee, population):
    column = f"ville_population_{annee}"
    with DatabaseConnection() as cursor:
        query = f"SELECT * FROM villes_france_free WHERE {column} >= %s"
        cursor.execute(query, (population,))
        result = cursor.fetchall()
    return jsonify(result) if result else handle_error(
        f"Aucune ville trouvée avec une population supérieure à {population} en {annee}"
    )

@app.route('/api/mock_data', methods=['GET'])
def get_mock_data():
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM MOCK_DATA")
        result = cursor.fetchall()
    return jsonify(result) if result else handle_error("Aucun enregistrement trouvé")

@app.route('/api/mock_data/<int:record_id>', methods=['GET'])
def get_mock_data_by_id(record_id):
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM MOCK_DATA WHERE id = %s", (record_id,))
        result = cursor.fetchone()
    return jsonify(result) if result else handle_error(f"Enregistrement avec l'ID {record_id} non trouvé")

@app.route('/api/mock_data', methods=['POST'])
def add_mock_data():
    data = request.get_json()
    with DatabaseConnection() as cursor:
        query = """
            INSERT INTO MOCK_DATA (first_name, last_name, email, gender, ip_address)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('first_name'), data.get('last_name'),
            data.get('email'), data.get('gender'), data.get('ip_address')
        ))
    return jsonify({"message": "Enregistrement ajouté avec succès"}), 201

@app.route('/api/mock_data/<int:record_id>', methods=['PUT'])
def update_mock_data(record_id):
    data = request.get_json()
    with DatabaseConnection() as cursor:
        query = """
            UPDATE MOCK_DATA
            SET first_name = %s, last_name = %s, email = %s, gender = %s, ip_address = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            data.get('first_name'), data.get('last_name'),
            data.get('email'), data.get('gender'), data.get('ip_address'),
            record_id
        ))
    return jsonify({"message": "Enregistrement mis à jour avec succès"}), 200

@app.route('/api/mock_data/<int:record_id>', methods=['DELETE'])
def delete_mock_data(record_id):
    with DatabaseConnection() as cursor:
        cursor.execute("DELETE FROM MOCK_DATA WHERE id = %s", (record_id,))
    return jsonify({"message": "Enregistrement supprimé avec succès"}), 200

if __name__ == '__main__':
    app.run(debug=True)
