from bitcash import Key
import requests
from telegram import ParseMode
from db.get import get_address, get_wif
from db.init import create_user
import checks
from settings import FEE_ADDRESS, FEE_PERCENTAGE


RATE_API = 'https://www.bitcoin.com/special/rates.json'


def start(bot, update):
    """ Starts the bot.
    Create a database entry for [username] unless it exists already.
    """
    if not checks.check_username(update):
        return
    first_name = update.message.from_user.first_name
    info = '. Type /help for the list of commands.'

    created = create_user(update.message.from_user.username)
    if created:
        return update.message.reply_text('Hello ' + first_name + info)
    else:
        return update.message.reply_text('Hello again, ' + first_name + info)


def deposit(bot, update):
    """
    Fetches and returns the Bitcoin Cash address saved in the db if the command
    was sent in a direct message. Asks to send DM otherwise.
    """
    if not checks.check_username(update):
        return
    if update.message.chat.type != 'private':  # check if in DM
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text='Private message me to see your deposit address')

    create_user(update.message.from_user.username)  # check if user is created
    address = get_address(update.message.from_user.username)
    update.message.reply_text('Send Bitcoin Cash to:')
    return update.message.reply_html('<b>{}</b>'.format(address))


def balance(bot, update):
    """ Fetches and returns the balance (in USD) """
    if not checks.check_username(update):
        return
    create_user(update.message.from_user.username)
    # get USD rate
    endpoint = RATE_API
    r = requests.get(endpoint)
    if r.status_code != 200:
        return update.message.reply_text(f'Unable to contact {endpoint}')
    data = r.json()
    rate = data[2]['rate'] / data[1]['rate']
    # get address balance in satoshi
    address = get_address(update.message.from_user.username)
    endpoint = ('https://rest.bitcoin.com/v2/address/details/' + address)
    r = requests.get(endpoint)
    if r.status_code != 200:
        return update.message.reply_text(f'Unable to contact {endpoint}')
    data = r.json()
    # calculate balance in USD
    balance_raw = (data['balance'] + data['unconfirmedBalance']) * rate
    balance = round(balance_raw, 2)

    return update.message.reply_text('You have: $' + str(balance))


def withdraw(bot, update, args):
    """ Withdraws BCH to user's wallet """
    if not checks.check_username(update):
        return

    if update.message.chat.type != 'private':  # check if in DM
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text='Private message me to withdraw your money')

    if len(args) != 2:
        return update.message.reply_text('Usage: /withdraw [amount] [address]')

    amount = args[0].replace('$', '')
    if not checks.amount_is_valid(amount):
        return update.message.reply_text(amount + ' is not a valid amount')

    sent_amount = float(amount) - 0.01  # after 1 cent fee

    address = args[1]
    if len(address) != 54 and len(address) != 42:
        message = f'{address} is not a valid Bitcoin Cash address.'
        return update.message.reply_text(message)
    if 'bitcoincash:' not in address:
        address = 'bitcoincash:' + address

    wif = get_wif(update.message.from_user.username)
    key = Key(wif)

    outputs = [
        (address, sent_amount, 'usd'),
        # add more recipients here
    ]
    key.get_balance()
    try:
        tx_id = key.send(outputs, fee=1)
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
/tip - Sends a tip. Usage: /tip [amount] [@username]
/price - Displays the current price of Bitcoin Cash""")


def tip(bot, update, args):
    """ Sends Bitcoin Cash on-chain """
    if not checks.check_username(update):
        return

    if len(args) != 2 and not update.message.reply_to_message:
        return update.message.reply_text('Usage: /tip [amount] [username]')

    if '@' in args[0]:
        tmp = args[1]
        args[1] = args[0]
        args[0] = tmp

    amount = args[0].replace('$', '')
    if not checks.amount_is_valid(amount):
        return update.message.reply_text(amount + ' is not a valid amount.')

    if update.message.reply_to_message:
        recipient_username = update.message.reply_to_message.from_user.username
        if not recipient_username:
            return update.message.reply_text(
                'You cannot tip someone who has not set a username.'
            )
    else:
        recipient_username = args[1]
        if not checks.username_is_valid(recipient_username):
            return update.message.reply_text(
                recipient_username + ' is not a valid username.')

    recipient_username = recipient_username.replace('@', '')
    sender_username = update.message.from_user.username

    if recipient_username == sender_username:
        return update.message.reply_text('You cannot send money to yourself.')

    create_user(recipient_username)  # IMPROVE
    recipient_address = get_address(recipient_username)
    sender_wif = get_wif(sender_username)

    key = Key(sender_wif)
    balance = key.get_balance('usd')
    # checks the balance
    if float(amount) > float(balance):
        return update.message.reply_text('You don\'t have enough funds! ' +
                                         'Type /deposit to add funds!!')

    fee = float(amount) * FEE_PERCENTAGE
    sent_amount = float(amount) - 0.01

    if fee < 0.01:
        outputs = [
            (recipient_address, sent_amount, 'usd'),
        ]
    else:
        sent_amount -= fee  # deducts fee
        outputs = [
            (recipient_address, sent_amount, 'usd'),
            (FEE_ADDRESS, fee, 'usd'),
        ]

    try:
        tx_id = key.send(outputs, fee=1)
    except:
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text='Transaction failed!',
            parse_mode=ParseMode.MARKDOWN)

    return bot.send_message(
        chat_id=update.effective_chat.id,
        text='You sent $' + amount + ' to ' + recipient_username,
        parse_mode=ParseMode.MARKDOWN)


def price(bot, update):
    """ Fetches and returns the price of BCH (in USD) """
    endpoint = RATE_API
    try:
        req = requests.get(endpoint)
    except:
        return update.message.reply_text('Error while fetching Bitcoin.com API')

    rate_list = req.json()
    bch_btc_rate, btc_usd_rate = rate_list[1]['rate'], rate_list[2]['rate']
    bch_price = round(btc_usd_rate / bch_btc_rate, 2)

    return bot.send_message(
        chat_id=update.effective_chat.id,
        text='1 BCH = US$' + str(bch_price),
        parse_mode=ParseMode.MARKDOWN)
