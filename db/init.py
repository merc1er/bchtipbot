import sqlite3
import os.path
from bitcash import Key


def init_database(database_name):
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
