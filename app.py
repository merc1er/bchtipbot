from telegram.ext import Updater, CommandHandler
import sqlite3
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Init the database
# cursor.execute("""CREATE TABLE users(
#     id INTEGER,
#     balance REAL
# )""")
# conn.commit()


TEST_ADDRESS = 'bitcoincash:qp07y2dy5jvcpfgssfalajytm3xg7yz5fye2gu5cz9'


def start(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def deposit(bot, update):
    update.message.reply_text(TEST_ADDRESS)


def balance(bot, update):
    # conn = sqlite3.connect('db.sqlite3')
    # cursor = conn.cursor()
    # query = ('SELECT balance FROM users WHERE id={}').format(
    #                                             update.message.from_user.id)
    # balance = cursor.execute(query)

    balance = 0

    update.message.reply_text('You have: ' + str(balance) + ' BCH')


def withdraw(bot, update):
    update.message.reply_text('I cannot do that yet 😅')


updater = Updater('892772409:AAGQk_Fyz3Uelwvhoq8yUmRXPUuTxnFFIfY')

# Commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('deposit', deposit))
updater.dispatcher.add_handler(CommandHandler('balance', balance))
updater.dispatcher.add_handler(CommandHandler('withdraw', withdraw))

updater.start_polling()
updater.idle()

# Update this later
conn.close()
