class MockData(BaseModel):
    id = AutoField()
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = CharField(max_length=255)
    gender = CharField(max_length=50)
    ip_address = CharField(max_length=50)

    class Meta:
        table_name = 'MOCK_DATA'
