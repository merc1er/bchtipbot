from peewee import *
from settings import DATABASE_PINK


db = SqliteDatabase(DATABASE_PINK)

class User(Model):
    username = CharField(max_length=30, unique=True)
    bch_address = CharField(max_length=54, unique=True)
    wif = CharField(max_length=54, unique=True)

    class Meta:
        database = db

