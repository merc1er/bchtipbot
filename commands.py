from bitcash import Key
from db.get import get_balance, get_address, get_wif
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
    return update.message.reply_html('<b>{}</b>'.format(address))


def balance(bot, update):
    """ Fetches and returns the balance (in satoshis) """
    create_user(update.message.from_user.username)
    balance = get_balance(update.message.from_user.username)
    return update.message.reply_text('You have: $' + balance)


def withdraw(bot, update, args):
    """ Withdraws BCH to user's wallet """
    if len(args) != 2:
        return update.message.reply_text('Usage: /withdraw [amount] [address]')

    amount = args[0].replace('$', '')
    if not amount_is_valid(amount):
        return update.message.reply_text(amount + ' is not a valid amount')

    sent_amount = float(amount) - 0.01  # after 1 cent fee

    address = args[1]
    # check if address is correct here?

    wif = get_wif(update.message.from_user.username)
    key = Key(wif)

    outputs = [
        (address, sent_amount, 'usd'),
        # add more recipients here
    ]
    key.get_balance()
    try:
        tx_id = key.send(outputs)
    except:
        return update.message.reply_text('Transaction failed!')

    return update.message.reply_text('Sent! Transaction ID: ' + tx_id)


def help_command(bot, update):
    """ Displays the help text """
    return update.message.reply_text("""/start - Starts the bot
/deposit - Displays your Bitcoin Cash address for top up
/balance - Shows your balance in Bitcoin Cash
/withdraw - Withdraw your funds. Usage: /withdraw $[amount] [address]
/help - Lists all commands
/tip - Sends a tip. Usage: /tip [amount] [@username]""")


def tip(bot, update, args):
    """ Sends Bitcoin Cash off-chain """
    if len(args) != 2:
        return update.message.reply_text('Usage: /tip [amount] [username]')

    amount = args[0].replace('$', '')
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

    recipient_address = get_address(recipient_username)
    sender_wif = get_wif(sender_username)

    key = Key(sender_wif)

    sent_amount = float(amount) - 0.01

    outputs = [
        (recipient_address, sent_amount, 'usd'),
        # add more recipients here (fee)
    ]
    key.get_balance()
    try:
        tx_id = key.send(outputs)
    except:
        return update.message.reply_text('Transaction failed!')

    return update.message.reply_text('You sent $' +
            amount + ' to ' + recipient_username)

