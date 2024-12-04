import os
import mysql.connector
from mysql.connector import Error

# Connexion à la base de données avec les variables d'environnement
connection = None
try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'root'),
        database=os.getenv('DB_NAME', 'francedb')
    )

    if connection.is_connected():
        print("Connexion réussie à la base de données MySQL")

        # Récupérer les départements
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM departement LIMIT 10;")
        departements_result = cursor.fetchall()

        print("Voici les départements :")
        for departement in departements_result:
            print(departement)

        # Récupérer les villes (table villes_france_free)
        try:
            cursor.execute("SELECT * FROM villes_france_free LIMIT 10;")
            villes_result = cursor.fetchall()

            print("Voici les villes :")
            for ville in villes_result:
                print(ville)
        except Error as e:
            print(f"Erreur lors de la récupération des villes : {e}")

except Error as e:
    print(f"Erreur lors de la connexion à MySQL : {e}")

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion MySQL fermée")
