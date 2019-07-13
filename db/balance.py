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
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ("""UPDATE users
        SET balance = balance {operator} {amount} 
        WHERE username="{username}" """).format(operator=operator,
                                            amount=amount, username=username)
    cursor.execute(query)
    conn.commit()
    conn.close()

    return True


def add(username, amount):
    """ Adds [amount] BCH to [username] """
    return update_balance(username, amount, operator='+')


def deduct(username, amount):
    """ Removes [amount] BCH to [username] if the remaining balance
    is positive.
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = 'SELECT balance FROM users WHERE username="{}"'.format(username)
    balance = cursor.execute(query).fetchone()[0]
    remaining_balance = float(balance) - float(amount)
    if remaining_balance < 0:
        return 'Insufficient balance.'
    conn.close()

    return update_balance(username, amount, operator='-')


def add_and_create(username, amount):
    """ Same as add() but creates DB entry if username is not present """
    create_user(username)
    return update_balance(username, amount, operator='+')
