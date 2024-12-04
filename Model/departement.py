from peewee import Model, CharField, MySQLDatabase

# Configuration de la base de données
database = MySQLDatabase(
    'francedb', 
    user='root',
    password='root',
    host='localhost',
    port=3306
)

# Définition du modèle
class BaseModel(Model):
    class Meta:
        database = database

class Departement(BaseModel):
    nom = CharField(max_length=255)
    description = CharField(max_length=500)

# Création de la table
if __name__ == "__main__":
    database.connect()
    database.create_tables([Departement])
    print("La table 'departements' a été créée avec succès !")
