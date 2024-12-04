# Projet MySQL Flask API

Ce projet propose une API REST basée sur Flask et connectée à une base de données MySQL. L'API permet de récupérer des informations sur les départements et les villes en France. Elle est conçue pour interroger les tables `departement` et `villes_france_free` et `MOCK_DATA`.

## Prérequis

Pour exécuter ce projet, vous aurez besoin de :
- **Python 3.13+**
- **MySQL 8.0+**
- **Flask** et **pymysql**
- Un serveur MySQL fonctionnel avec des tables `departement` et `villes_france_free` correctement configurées.

## Installation

1. Clonez ce dépôt sur votre machine locale :
   ```bash
   git clone https://github.com/James-TREMA/MYSQL.git
   cd MYSQL
   ```

2. Installez les dépendances Python dans un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Linux/MacOS
   venv\Scripts\activate     # Sous Windows
   pip install -r requirements.txt
   ```

3. Configurez votre base de données MySQL avec les tables nécessaires. Voici les structures de tables attendues :
   - **Table `departement` :**
     ```
     departement_id            INT AUTO_INCREMENT PRIMARY KEY
     departement_code          VARCHAR(10)
     departement_nom           VARCHAR(100)
     departement_nom_uppercase VARCHAR(100)
     departement_slug          VARCHAR(100)
     departement_nom_soundex   VARCHAR(50)
     ```
   - **Table `villes_france_free` :**
     ```
     ville_id              INT AUTO_INCREMENT PRIMARY KEY
     ville_departement     VARCHAR(10)
     ville_slug            VARCHAR(255)
     ville_nom             VARCHAR(255)
     ville_nom_simple      VARCHAR(255)
     ville_nom_reel        VARCHAR(255)
     ville_nom_soundex     VARCHAR(50)
     ville_nom_metaphone   VARCHAR(50)
     ville_code_postal     VARCHAR(20)
     ville_commune         VARCHAR(50)
     ville_code_commune    VARCHAR(50)
     ville_population_2010 INT
     ville_population_1999 INT
     ```
   - **Table `MOCK_DATA` :**
     ```
     id           INT
     first_name   VARCHAR(50)
     last_name    VARCHAR(50)
     email        VARCHAR(50)
     gender       VARCHAR(50)
     ip_address   VARCHAR(20)
     ```

4. Lancez le serveur Flask :
   ```bash
   py venv/Scripts/server.py
   ```

## Commandes CURL pour tester l'API

### **Endpoints pour les départements**

1. Récupérer tous les départements :
   ```bash
   curl http://127.0.0.1:5000/api/departements
   ```

2. Récupérer un département par ID :
   ```bash
   curl http://127.0.0.1:5000/api/departements/1
   ```

3. Récupérer un département par code :
   ```bash
   curl http://127.0.0.1:5000/api/departements/code/01
   ```

### **Endpoints pour les villes**

4. Récupérer les villes d'un département :
   ```bash
   curl http://127.0.0.1:5000/api/villes/departement/75
   ```

5. Récupérer les villes par nom :
   ```bash
   curl http://127.0.0.1:5000/api/villes/nom/Paris
   ```

6. Récupérer les villes par code postal :
   ```bash
   curl http://127.0.0.1:5000/api/villes/code_postal/75000
   ```

7. Récupérer les villes avec une population minimale :
   ```bash
   curl http://127.0.0.1:5000/api/villes/population/2010/5000
   ```

### **Endpoints pour la table**

8. **Récupérer tous les enregistrements :**
   ```bash
   curl http://127.0.0.1:5000/api/mock_data
   ```

9. **Récupérer un enregistrement par ID :**
   ```bash
   curl http://127.0.0.1:5000/api/mock_data/1
   ```

10. **Ajouter un nouvel enregistrement :**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "gender": "Male", "ip_address": "192.168.1.1"}' http://127.0.0.1:5000/api/mock_data
   ```

11. **Mettre à jour un enregistrement :**
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com", "gender": "Female", "ip_address": "192.168.1.2"}' http://127.0.0.1:5000/api/mock_data/1
   ```

12. **Supprimer un enregistrement :**
   ```bash
   curl -X DELETE http://127.0.0.1:5000/api/mock_data/1
   ```


## Organisation des fichiers

- **`server.py` :** Contient la logique backend de l'API Flask.
- **`test_routes.py` :** Script pour tester les différents endpoints de l'API.
- **`data_departements.sql` et `data_villes.sql` :** Scripts SQL pour remplir les tables avec des données.

## Exécution des tests

Pour exécuter les tests des endpoints, lancez simplement le fichier `test_routes.py` :
```bash
py venv/Scripts/test_routes.py
```

## Résultats attendus

- Les réponses des endpoints sont formatées en JSON.
- En cas de succès, vous recevez les données demandées.
- En cas d'erreur, un message approprié est retourné, par exemple :
  ```json
  {"error": "Département avec l'ID 1 non trouvé"}
  ```

## Contribution

Les contributions sont les bienvenues. Merci de soumettre une pull request pour toute amélioration ou correction.

---

### **Instructions**
1. Sauvegardez ce contenu dans un fichier nommé `README.md` à la racine de votre projet.
2. Vérifiez si des détails supplémentaires spécifiques à votre projet doivent être ajoutés. 
3. Partagez ce fichier avec vos collègues ou utilisateurs pour leur permettre de comprendre et tester l'API.