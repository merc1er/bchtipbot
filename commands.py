from bitcash import Key
from db.balance import (add, deduct, add_and_create,
                        get_balance, get_address, get_wif)
from db.init import create_user
from checks import *


def start(bot, update):
    """ Starts the bot.
    Create a database entry for [username] unless it exists already.
    """
    first_name = update.message.from_user.first_name

    created = create_user(update.message.from_user.username)
    if created:
        return update.message.reply_text('Hello ' + first_name)
    else:
        return update.message.reply_text('Hello again, ' + first_name)


def deposit(bot, update):
    """ Fetches and returns the Bitcoin Cash address saved in the db """
    create_user(update.message.from_user.username)
    address = get_address(update.message.from_user.username)
    update.message.reply_text('Send Bitcoin Cash to:')
    update.message.reply_html('<b>{}</b>'.format(address))
    return update.message.reply_text('Then type /deposited')


def deposited(bot, update):
    """ TODO """
    wif = get_wif(update.message.from_user.username)
    # check if a payment was made
    # if so, increase balance
    return update.message.reply_text('WIP')


def balance(bot, update):
    """ Fetches and returns the balance (in BCH) saved in the db """
    create_user(update.message.from_user.username)
    balance = get_balance(update.message.from_user.username)
    return update.message.reply_text(
                                'You have: ' + balance + ' satoshis')


def withdraw(bot, update, args):
    """ TODO """
    # check if amount is correct
    # check if address is correct
    # deduct amount from user
    # sends amount (- tx fee) to the address
    return update.message.reply_text('I cannot do that yet 😅')


def help_command(bot, update):
    """ Displays the help text """
    return update.message.reply_text("""/start - Starts the bot
/deposit - Displays your Bitcoin Cash address for top up
/balance - Shows your balance in Bitcoin Cash
/withdraw - Withdraw your funds. Usage: /withdraw [amount] [address]
/help - Lists all commands
/tip - Sends a tip. Usage: /tip [amount] [@username]""")


def tip(bot, update, args):
    """ Sends Bitcoin Cash off-chain """
    if len(args) != 2:
        return update.message.reply_text('Usage: /tip [amount] [username]')

    amount = args[0]
    if not amount_is_valid(amount):
        return update.message.reply_text(amount + ' is not a valid amount.')

    recipient_username = args[1]
    if not username_is_valid(recipient_username):
        return update.message.reply_text(
                    recipient_username + ' is not a valid username.')

    recipient_username = recipient_username[1:]  # remove the '@'
    sender_username = update.message.from_user.username

    if recipient_username == sender_username:
        return update.message.reply_text('You cannot send money to yourself.')

    # deduct from sender and add to recipient
    response = deduct(sender_username, amount)
    if response != True:
        # checks if the sender has enough money
        return update.message.reply_text(response)
    add_and_create(recipient_username, amount)

    return update.message.reply_text(
        'You sent ' + f'{int(amount):,}' + ' satoshis to ' + recipient_username)


def add_funds(bot, update):  # REMOVE BEFORE DEPLOYING
    """ Adds funds (100 fake BCH)
    This is for testing only!
    """
    amount = 100000000  # adds 1 BCH
    add(update.message.from_user.username, amount)
    return update.message.reply_text(f'{amount:,}' + ' BCH added')

