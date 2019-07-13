import sqlite3
from .init import create_user
from .models import db, User
from bitcash import Key
from settings import DATABASE_PINK


def get_balance(username):
    """ Returns the balance (float) or [username] """
    db.connect(reuse_if_open=True)
    balance = User.get(User.username == username).balance
    db.close()

    return balance


def get_address(username):
    """ Returns the Bitcoin Cash address (str) of [username] """
    db.connect()
    address = User.get(User.username == username).bch_address
    db.close()

    return address


def update_balance(username, amount, operator):
    """ Updates (increase or decrease) the user's balance """
    db.connect(reuse_if_open=True)
    user = User.get(User.username == username)
    if operator == '+':
        user.balance += float(amount)
    else:
        user.balance -= float(amount)
    user.save()
    db.close()

    return True


def add(username, amount):
    """ Adds [amount] BCH to [username] """
    return update_balance(username, amount, operator='+')


def deduct(username, amount):
    """ Removes [amount] BCH to [username] if the remaining balance
    is positive.
    """
    db.connect(reuse_if_open=True)
    user = User.get(User.username == username)
    remaining_balance = user.balance - float(amount)
    db.close()

    if remaining_balance < 0:
        return 'Insufficient balance.'

    return update_balance(username, amount, operator='-')


def add_and_create(username, amount):
    """ Same as add() but creates DB entry if username is not present """
    create_user(username)
    return update_balance(username, amount, operator='+')
