import sqlite3
from bitcash import Key
from db.balance import add, deduct, add_and_create, get_balance, get_address
from db.init import create_user


# URL or filename for the main database
DATABASE_PINK = 'db.sqlite3'


def start(bot, update):
    """ Starts the bot.
    Create a database entry for [username] unless it exists already.
    """
    first_name = update.message.from_user.first_name

    created = create_user(update.message.from_user.username)
    if created:
        update.message.reply_text('Hello ' + first_name)
    else:
        update.message.reply_text('Hello again, ' + first_name)


def deposit(bot, update):
    """ Fetches and returns the Bitcoin Cash address saved in the db """
    address = get_address(update.message.from_user.username)
    update.message.reply_text(address)


def balance(bot, update):
    """ Fetches and returns the balance (in BCH) saved in the db """
    balance = get_balance(update.message.from_user.username)
    update.message.reply_text('You have: ' + str(balance) + ' BCH')


def withdraw(bot, update):
    """ TODO
    """
    update.message.reply_text('I cannot do that yet 😅')


def help_command(bot, update):
    """ Displays the help text """
    update.message.reply_text("""/start - Starts the bot
/deposit - Displays your Bitcoin Cash address for top up
/balance - Shows your balance in Bitcoin Cash
/withdraw - Withdraw your funds. Usage: /withdraw [amount] [address]
/help - Lists all commands
/tip - Sends a tip. Usage: /tip [amount] [@username]""")


def tip(bot, update, args):
    """ Sends Bitcoin Cash off-chain """
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
    # add (or create user if not in the DB) funds to the recipient
    add_and_create(recipient_username[1:], amount)

    update.message.reply_text(
        'You sent ' + amount + ' BCH to ' + recipient_username)


def add_funds(bot, update):  # REMOVE BEFORE DEPLOYING
    """ Adds funds (100 fake BCH)
    This is for testing only!
    """
    add(update.message.from_user.username, 100)

    update.message.reply_text('100 BCH added')

