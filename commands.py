import sqlite3
from bitcash import Key


# URL or filename for the main database
DATABASE_PINK = 'db.sqlite3'


def start(bot, update):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name

    # Check if user is already in the database
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT * FROM users WHERE id=' + str(user_id))
    response = cursor.execute(query).fetchone()

    if response:
        conn.close()
        update.message.reply_text('Hello again, ' + first_name)
    else:
        key = Key()
        context = (
            user_id,
            0,  # initial balance
            key.address,
            key.to_wif(),
        )

        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', context)
        conn.commit()
        conn.close()
        update.message.reply_text('Hello ' + first_name)


def deposit(bot, update):
    """ Fetches and returns the Bitcoin Cash address saved in the db
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT bch_address FROM users WHERE id={}').format(
                                                update.message.from_user.id)
    address = cursor.execute(query).fetchone()[0]

    update.message.reply_text(address)


def balance(bot, update):
    """ Fetches and returns the balance (in BCH) saved in the db
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT balance FROM users WHERE id={}').format(
                                                update.message.from_user.id)
    balance = cursor.execute(query).fetchone()[0]

    update.message.reply_text('You have: ' + str(balance) + ' BCH')


def withdraw(bot, update):
    """ TODO
    """
    update.message.reply_text('I cannot do that yet 😅')


def help_command(bot, update):
    """ Displays the help text
    """
    update.message.reply_text("""List of commands:
    /start
    /help
    /deposit
    /balance
    /withdraw [amount] [BCH address]
    /tip [amount] [username]""")


def tip(but, update, args):
    """ Sends Bitcoin Cash off-chain
    """
    if len(args) != 2:
        update.message.reply_text('Usage: /tip [amount] [username]')

    amount = args[0]
    sender_id = update.message.from_user.id
    recipient = args[1]

    update.message.reply_text('You sent ' + amount + ' BCH to ' + recipient)

