import requests

BASE_URL = "http://127.0.0.1:5000"

def perform_request(method, endpoint, **kwargs):
    """Effectue une requête HTTP et gère les erreurs."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, **kwargs)
        print(f"{method.upper()} {endpoint}: {response.status_code}")
        if response.headers.get('Content-Type') == 'application/json':
            print(response.json())
        else:
            print("Réponse non JSON:", response.text)
    except requests.RequestException as e:
        print(f"Erreur lors de la requête {method.upper()} {endpoint}: {e}")

# Tests pour les départements
def test_get_all_departements():
    perform_request("GET", "/api/departements")

def test_get_departement_by_id(departement_id=1):
    perform_request("GET", f"/api/departements/{departement_id}")

def test_get_departement_by_code(departement_code="01"):
    perform_request("GET", f"/api/departements/code/{departement_code}")

# Tests pour les villes
def test_get_villes_by_departement(departement_code="75"):
    perform_request("GET", f"/api/villes/departement/{departement_code}")

def test_get_villes_by_nom(ville_nom="Paris"):
    perform_request("GET", f"/api/villes/nom/{ville_nom}")

def test_get_villes_by_code_postal(code_postal="75000"):
    perform_request("GET", f"/api/villes/code_postal/{code_postal}")

def test_get_villes_by_population(annee=2010, population=5000):
    perform_request("GET", f"/api/villes/population/{annee}/{population}")

# Tests pour MOCK_DATA
def test_get_all_mock_data():
    perform_request("GET", "/api/mock_data")

def test_get_mock_data_by_id(record_id=1):
    perform_request("GET", f"/api/mock_data/{record_id}")

def test_add_mock_data():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "gender": "Male",
        "ip_address": "192.168.1.1"
    }
    perform_request("POST", "/api/mock_data", json=data)

def test_update_mock_data(record_id=1):
    data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "gender": "Female",
        "ip_address": "192.168.1.2"
    }
    perform_request("PUT", f"/api/mock_data/{record_id}", json=data)

def test_delete_mock_data(record_id=1):
    perform_request("DELETE", f"/api/mock_data/{record_id}")

if __name__ == "__main__":
    # Tests pour les départements
    test_get_all_departements()
    test_get_departement_by_id()
    test_get_departement_by_code()

    # Tests pour les villes
    test_get_villes_by_departement()
    test_get_villes_by_nom()
    test_get_villes_by_code_postal()
    test_get_villes_by_population()

    # Tests pour MOCK_DATA
    test_get_all_mock_data()
    test_get_mock_data_by_id()
    test_add_mock_data()
    test_update_mock_data()
    test_delete_mock_data()
