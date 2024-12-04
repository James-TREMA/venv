class Departement(BaseModel):
    departement_id = AutoField()
    departement_code = CharField(max_length=10)
    departement_name = CharField(max_length=255)

    class Meta:
        table_name = 'departement'
