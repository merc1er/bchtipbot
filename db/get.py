from .init import create_user
from .models import db, User
from bitcash import Key


def get_balance(username):
    """ Returns the balance (float) or [username] """
    wif = User.get(User.username == username).wif
    key = Key(wif)
    balance = key.get_balance()
    return balance


def get_address(username):
    """ Returns the Bitcoin Cash address (str) of [username] """
    address = User.get(User.username == username).bch_address
    return address


def get_wif(username):
    """ Returns the Wallet Import Format (str) of [username] """
    wif = User.get(User.username == username).wif
    return wif
