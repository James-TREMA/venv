from peewee import Model, CharField, MySQLDatabase

# Configuration de la base de données
database = MySQLDatabase(
    'francedb', 
    user='root',
    password='root',
    host='localhost',
    port=3306
)

# Définition du modèle de base
class BaseModel(Model):
    class Meta:
        database = database

# Modèle pour les départements
class Departement(BaseModel):
    code = CharField(max_length=10, unique=True)  # Ajout du code département
    nom = CharField(max_length=255)
    description = CharField(max_length=500, null=True)

    @classmethod
    def creer_departement(cls, code, nom, description=None):
        """Créer un nouveau département."""
        return cls.create(code=code, nom=nom, description=description)

    @classmethod
    def recuperer_par_code(cls, code):
        """Récupérer un département par son code."""
        return cls.get_or_none(cls.code == code)

    @classmethod
    def lister_tous(cls):
        """Lister tous les départements."""
        return list(cls.select())

# Création de la table
if __name__ == "__main__":
    database.connect()
    database.create_tables([Departement])
    print("La table 'departements' a été créée avec succès !")

    # Exemple d'ajout de départements
    Departement.creer_departement("75", "Paris", "Capitale de la France")
    Departement.creer_departement("13", "Bouches-du-Rhône", "Département du sud")
    print("Exemples de départements ajoutés.")
