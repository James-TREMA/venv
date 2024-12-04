from peewee import *
from Model.base import BaseModel 

# Configuration de la base de données
database = MySQLDatabase(
    'francedb',
    user='root',
    password='root',
    host='localhost',
    charset='utf8mb4'
)

class BaseModel(Model):
    class Meta:
        database = database
