class VillesFranceFree(BaseModel):
    ville_id = AutoField()
    ville_departement = CharField(max_length=10)
    ville_nom = CharField(max_length=255)
    ville_code_postal = CharField(max_length=20)
    ville_population = IntegerField()

    class Meta:
        table_name = 'villes_france_free'
