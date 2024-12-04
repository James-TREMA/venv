from peewee import *
from Model.base import BaseModel

class VillesFranceFree(Model):
    ville_id = AutoField()
    ville_departement = CharField(max_length=10, null=False)
    ville_slug = CharField(max_length=255, null=False)
    ville_nom_simple = CharField(max_length=255, null=False)
    ville_nom_reel = CharField(max_length=255, null=False)
    ville_nom_soundex = CharField(max_length=50, null=False)
    ville_nom_metaphone = CharField(max_length=50, null=False)
    ville_code_postal = CharField(max_length=20, null=False)
    ville_commune = CharField(max_length=50, null=False)
    ville_code_commune = CharField(max_length=50, null=False)
    ville_arrondissement = IntegerField(null=True)
    ville_canton = CharField(max_length=50, null=True)
    ville_amdi = IntegerField(null=True)
    ville_population_2010 = IntegerField(null=True)
    ville_population_1999 = IntegerField(null=True)
    ville_population_2012 = IntegerField(null=True)
    ville_densite_2010 = IntegerField(null=True)
    ville_surface = FloatField(null=True)
    ville_longitude_deg = FloatField(null=True)
    ville_latitude_deg = FloatField(null=True)
    ville_longitude_grd = CharField(max_length=50, null=True)
    ville_latitude_grd = CharField(max_length=50, null=True)
    ville_longitude_dms = CharField(max_length=50, null=True)
    ville_latitude_dms = CharField(max_length=50, null=True)
    ville_zmin = IntegerField(null=True)
    ville_zmax = IntegerField(null=True)

    class Meta:
        database = database
        table_name = 'villes_france_free'
