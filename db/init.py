import os.path
from bitcash import Key
from settings import DATABASE_PINK


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
