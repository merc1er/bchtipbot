from telegram.ext import Updater, CommandHandler
import sqlite3
from bitcash import Key  # unused
from db.init import init_database
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


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


# Main program
init_database(DATABASE_PINK)
updater = Updater('892772409:AAGQk_Fyz3Uelwvhoq8yUmRXPUuTxnFFIfY')

# Commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CommandHandler('deposit', deposit))
updater.dispatcher.add_handler(CommandHandler('balance', balance))
updater.dispatcher.add_handler(CommandHandler('withdraw', withdraw))

updater.start_polling()
updater.idle()
