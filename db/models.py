from peewee import *
from settings import DEBUG
import os
from urllib.parse import urlparse, uses_netloc


if DEBUG:
    db = SqliteDatabase('db.sqlite3')
else:
    uses_netloc.append('postgres')
    url = urlparse(os.environ['DATABASE_URL'])
    db = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )

class User(Model):
    username = CharField(max_length=30, unique=True)
    bch_address = CharField(max_length=54, unique=True)
    wif = CharField(max_length=54, unique=True)

    class Meta:
        database = db

