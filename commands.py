import sqlite3
from bitcash import Key
from db.balance import add, deduct


# URL or filename for the main database
DATABASE_PINK = 'db.sqlite3'


def start(bot, update):
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name

    # Check if user is already in the database
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT * FROM users WHERE username="' + str(username) + '"')
    response = cursor.execute(query).fetchone()

    if response:
        conn.close()
        update.message.reply_text('Hello again, ' + first_name)
    else:
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
        update.message.reply_text('Hello ' + first_name)


def deposit(bot, update):
    """ Fetches and returns the Bitcoin Cash address saved in the db
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT bch_address FROM users WHERE username="{}"').format(
                                            update.message.from_user.username)
    address = cursor.execute(query).fetchone()[0]

    update.message.reply_text(address)


def balance(bot, update):
    """ Fetches and returns the balance (in BCH) saved in the db
    """
    conn = sqlite3.connect(DATABASE_PINK)
    cursor = conn.cursor()
    query = ('SELECT balance FROM users WHERE username="{}"').format(
                                            update.message.from_user.username)
    balance = cursor.execute(query).fetchone()[0]
    conn.close()

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


def tip(bot, update, args):
    """ Sends Bitcoin Cash off-chain
    """
    if len(args) != 2:
        update.message.reply_text('Usage: /tip [amount] [username]')

    amount = args[0]
    sender_username = update.message.from_user.username
    recipient_username = args[1]
    # check recipient's username
    if recipient_username[0] != '@':
        update.message.reply_text(
            recipient_username + ' is not a valid username')

    # deduct the amount from the sender
    deduct(sender_username, amount)

    update.message.reply_text(
        'You sent ' + amount + ' BCH to ' + recipient_username)


def add_funds(bot, update):  # REMOVE BEFORE DEPLOYING
    """ Adds funds (100 fake BCH)
    This is for testing only!
    """
    add(update.message.from_user.username, 100)

    update.message.reply_text('100 BCH added')

