from .models import User


def get_address(username):
    """ Returns the Bitcoin Cash address (str) of [username] """
    address = User.get(User.username == username).bch_address
    return address


def get_wif(username):
    """ Returns the Wallet Import Format (str) of [username] """
    wif = User.get(User.username == username).wif
    return wif


def count_users():
    """ Returns the number of initialised users """
    return User.select().count()
