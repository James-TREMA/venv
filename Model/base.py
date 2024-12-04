from peewee import *

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
