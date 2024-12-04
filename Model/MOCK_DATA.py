from peewee import *
from Model.base import BaseModel

class MockData(BaseModel):
    id = AutoField()
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    email = CharField(max_length=50, null=False)
    gender = CharField(max_length=50, null=False)
    ip_address = CharField(max_length=20, null=False)

    class Meta:
        database = database
        table_name = 'MOCK_DATA'
