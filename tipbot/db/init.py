from bitcash import Key
from peewee import IntegrityError
from .models import db, User


def create_user(username):
    """ Checks if a Telegram user is present in the database.
    Returns True if a user is created, False otherwise.
    """
    db.connect(reuse_if_open=True)
    key = Key()
    try:
        User.create(username=username, bch_address=key.address, wif=key.to_wif())
        db.close()
        return True
    except IntegrityError:
        db.close()
        return False
