import sqlite3


DATABASE_PINK = 'db.sqlite3'  # improve this


def update_balance(user_id, amount, operator):
    """ Updates (increase or decrease) the user's balance
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ("""UPDATE users
        SET balance = balance {operator} {amount} 
        WHERE id={user_id}""").format(operator=operator,
                                            amount=amount, user_id=user_id)
    cursor.execute(query)
    conn.commit()
    conn.close()

    return True


def add(user_id, amount):
    return update_balance(user_id, amount, operator='+')


def deduct(user_id, amount):
    return update_balance(user_id, amount, operator='-')
