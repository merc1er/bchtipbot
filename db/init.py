import sqlite3
import os.path
from bitcash import Key


# URL or filename for the main database
DATABASE_PINK = 'db.sqlite3'  # improve this


def init_database(database_name=DATABASE_PINK):
    """ Checks if a local SQLite3 database is present.
    Returns False if the file already exists, True otherwise.
    """
    if not os.path.isfile(database_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE users(
            username TEXT NOT NULL,
            balance REAL NOT NULL,
            bch_address TEXT NOT NULL,
            wif TEXT NOT NULL
        )""")
        conn.commit()
        conn.close()
        return True

    return False


def create_user(username):
    """ Checks if a Telegram user is present in the database.
    Returns True if a user is created, False otherwise.
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()

    query = ('SELECT * FROM users WHERE username="' + username + '"')
    entry = cursor.execute(query).fetchone()

    # if user is not present in the database
    if not entry:
        key = Key()
        context = (
            username,
            0,  # initial balance
            key.address,
            key.to_wif(),
        )

        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', context)
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False
