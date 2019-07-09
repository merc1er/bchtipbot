from telegram.ext import Updater, CommandHandler
# import sqlite3


TEST_ADDRESS = 'bitcoincash:qp07y2dy5jvcpfgssfalajytm3xg7yz5fye2gu5cz9'


def start(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def deposit(bot, update):
    update.message.reply_text(TEST_ADDRESS)


def withdraw(bot, update):
    update.message.reply_text('I cannot do that yet 😅')


updater = Updater('892772409:AAGQk_Fyz3Uelwvhoq8yUmRXPUuTxnFFIfY')

# Commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('deposit', deposit))
updater.dispatcher.add_handler(CommandHandler('withdraw', withdraw))

updater.start_polling()
updater.idle()

# conn = sqlite3.connect('db.sqlite3')

# cursor = conn.cursor()

# # cursor.execute("""CREATE TABLE users(
# #     username TEXT,
# #     balance REAL
# # )""")
# # conn.commit()

# conn.close()
