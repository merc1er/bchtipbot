import sqlite3
import os.path


def init_database(database_name):
    if not os.path.isfile(database_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE users(
            id INTEGER,
            balance REAL
        )""")
        conn.commit()
        conn.close()
        return True

    return False
