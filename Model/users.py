from peewee import *
from Model.base import BaseModel

class MockData(BaseModel):  # Modèle pour représenter la table 'MOCK_DATA'
    id = AutoField()
    first_name = CharField(max_length=50, null=False)  # Prénom
    last_name = CharField(max_length=50, null=False)   # Nom de famille
    email = CharField(max_length=50, null=False, unique=True)  # Email
    gender = CharField(max_length=50, null=False)  # Genre
    ip_address = CharField(max_length=20, null=False)  # Adresse IP

    class Meta:
        table_name = 'MOCK_DATA'
