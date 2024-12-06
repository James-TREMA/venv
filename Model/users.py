from peewee import *
from Model.base import BaseModel

class User(BaseModel):
    id = AutoField()
    username = CharField(max_length=50, null=False, unique=True)  # Nom d'utilisateur
    email = CharField(max_length=100, null=False, unique=True)   # Adresse email
    password = CharField(max_length=255, null=False)             # Mot de passe (haché)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])  # Date de création

    class Meta:
        table_name = 'users'
