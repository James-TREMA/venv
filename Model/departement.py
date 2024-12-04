from peewee import *
from Model.base import BaseModel  # Utiliser BaseModel pour inclure database

class Departement(BaseModel):  # BaseModel inclut déjà la base de données
    departement_id = AutoField()
    departement_code = CharField(max_length=10, null=False)
    departement_nom = CharField(max_length=100, null=False)
    departement_nom_uppercase = CharField(max_length=100, null=False)
    departement_slug = CharField(max_length=100, null=False)
    departement_nom_soundex = CharField(max_length=50, null=False)

    class Meta:
        table_name = 'departement'
