from peewee import *
from Scripts.server import database  # Reuse the database connection from server.py

class Departement(Model):
    departement_id = AutoField()
    departement_code = CharField(max_length=10, null=False)
    departement_nom = CharField(max_length=100, null=False)
    departement_nom_uppercase = CharField(max_length=100, null=False)
    departement_slug = CharField(max_length=100, null=False)
    departement_nom_soundex = CharField(max_length=50, null=False)

    class Meta:
        database = database
        table_name = 'departement'
