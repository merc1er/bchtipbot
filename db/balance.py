from .init import create_user
from .models import db, User
from bitcash import Key
from settings import DATABASE_PINK


def get_balance(username):
    """ Returns the balance (float) or [username] """
    balance = User.get(User.username == username).balance
    return balance


def get_address(username):
    """ Returns the Bitcoin Cash address (str) of [username] """
    address = User.get(User.username == username).bch_address
    return address


def update_balance(username, amount, operator):
    """ Updates (increase or decrease) the user's balance """
    user = User.get(User.username == username)
    if operator == '+':
        user.balance += float(amount)
    else:
        user.balance -= float(amount)
    user.save()
    return True


def add(username, amount):
    """ Adds [amount] BCH to [username] """
    return update_balance(username, amount, operator='+')


def deduct(username, amount):
    """ Removes [amount] BCH to [username] if the remaining balance
    is positive.
    """
    user = User.get(User.username == username)
    remaining_balance = user.balance - float(amount)

    if remaining_balance < 0:
        return 'Insufficient balance.'
    return update_balance(username, amount, operator='-')


def add_and_create(username, amount):
    """ Same as add() but creates DB entry if username is not present """
    create_user(username)
    return update_balance(username, amount, operator='+')
