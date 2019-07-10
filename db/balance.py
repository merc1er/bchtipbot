import sqlite3
from .init import create_user
from bitcash import Key


DATABASE_PINK = 'db.sqlite3'  # improve this


def get_balance(username):
    """ Returns the balance (float) or [username] """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT balance FROM users WHERE username="{}"').format(username)
    balance = cursor.execute(query).fetchone()[0]
    conn.close()

    return balance


def get_address(username):
    """ Returns the Bitcoin Cash address (str) of [username] """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT bch_address FROM users WHERE username="{}"').format(
                                                                    username)
    address = cursor.execute(query).fetchone()[0]

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
