from bitcash import Key
from telegram import ParseMode
from db.get import get_address, get_wif
from db.init import create_user
import checks
from settings import FEE_ADDRESS, FEE_PERCENTAGE
from rates import get_rate


def start(bot, update):
    """ Starts the bot.
    Create a database entry for [username] unless it exists already.
    """
    if not checks.check_username(update):
        return
    first_name = update.message.from_user.first_name
    info = ". Type /help for the list of commands."

    created = create_user(update.message.from_user.username)
    if created:
        return update.message.reply_text("Hello " + first_name + info)
    else:
        return update.message.reply_text("Hello again, " + first_name + info)


def deposit(bot, update):
    """
    Fetches and returns the Bitcoin Cash address saved in the db if the command
    was sent in a direct message. Asks to send DM otherwise.
    """
    if not checks.check_username(update):
        return
    if update.message.chat.type != "private":  # check if in DM
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text="Private message me to see your deposit address",
        )

    create_user(update.message.from_user.username)  # check if user is created
    address = get_address(update.message.from_user.username)
    update.message.reply_text("Send Bitcoin Cash to:")
    return update.message.reply_html("<b>{}</b>".format(address))


def balance(bot, update):
    """ Fetches and returns the balance (in USD) """
    if not checks.check_username(update):
        return
    create_user(update.message.from_user.username)
    key = Key(get_wif(update.message.from_user.username))
    balance = key.get_balance("usd")
    return update.message.reply_text("You have: $" + str(balance))


def withdraw(bot, update, args):
    """ Withdraws BCH to user's wallet """
    if not checks.check_username(update):
        return

    if update.message.chat.type != "private":  # check if in DM
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text="Private message me to withdraw your money",
        )

    if len(args) != 2:
        message = (
            "Usage: /withdraw [amount] [address]\n\n"
            "You may also withdraw everything at once using:"
            " /withdraw all [address]"
        )
        return update.message.reply_text(message)

    address = checks.check_address(update, args[1])
    if not address:  # does not send anything if address is False
        return

    wif = get_wif(update.message.from_user.username)
    key = Key(wif)

    if args[0] == "all":
        sent_amount = 1000
        currency = "satoshi"
    else:
        amount = args[0].replace("$", "")
        if not checks.amount_is_valid(amount):
            return update.message.reply_text(amount + " is not a valid amount")
        currency = "usd"
        sent_amount = float(amount) - 0.01  # after 1 cent fee

    outputs = [
        (address, sent_amount, currency),
    ]
    key.get_unspents()
    try:
        if args[0] == "all":
            tx_id = key.send(outputs, fee=1, leftover=address)
        else:
            tx_id = key.send(outputs, fee=1)
    except Exception:
        return update.message.reply_text("Transaction failed!")

    return update.message.reply_text("Sent! Transaction ID: " + tx_id)


def help_command(bot, update):
    """ Displays the help text """
    return update.message.reply_text(
        """/start - Starts the bot
/deposit - Displays your Bitcoin Cash address for top up
/balance - Shows your balance in Bitcoin Cash
/withdraw - Withdraw your funds. Usage: /withdraw [amount] [address]
/help - Lists all commands
/tip - Sends a tip. Usage: /tip [amount] [@username]
/price - Displays the current price of Bitcoin Cash"""
    )


def tip(bot, update, args, satoshi=False):
    """ Sends Bitcoin Cash on-chain """
    if not checks.check_username(update):
        return

    try:  # in case the user wants to tip satoshis
        if args[1] == "satoshi" or args[1] == "satoshis":
            satoshi = True
            args[1] = args[2]
    except IndexError:
        pass

    if len(args) < 2 and not update.message.reply_to_message:
        return update.message.reply_text("Usage: /tip [amount] [username]")

    if "@" in args[0]:
        # this swaps args[0] and args[1] in case user input username before
        # amount (e.g. /tip @merc1er $1) - the latter will still work
        tmp = args[1]
        args[1] = args[0]
        args[0] = tmp

    amount = args[0].replace("$", "")
    if not checks.amount_is_valid(amount):
        return update.message.reply_text(amount + " is not a valid amount.")

    if update.message.reply_to_message:
        recipient_username = update.message.reply_to_message.from_user.username
        if not recipient_username:
            return update.message.reply_text(
                "You cannot tip someone who has not set a username."
            )
    else:
        recipient_username = args[1]
        if not checks.username_is_valid(recipient_username):
            return update.message.reply_text(
                recipient_username + " is not a valid username."
            )

    recipient_username = recipient_username.replace("@", "")
    sender_username = update.message.from_user.username

    if recipient_username == sender_username:
        return update.message.reply_text("You cannot send money to yourself.")

    create_user(recipient_username)  # IMPROVE
    recipient_address = get_address(recipient_username)
    sender_wif = get_wif(sender_username)

    key = Key(sender_wif)
    balance = key.get_balance("usd")
    # checks the balance
    if float(amount) > float(balance) and not satoshi:
        return update.message.reply_text(
            "You don't have enough funds! " + "Type /deposit to add funds!!"
        )

    fee = float(amount) * FEE_PERCENTAGE
    sent_amount = float(amount) - 0.01

    if satoshi:  # if user is sending satoshis
        outputs = [(recipient_address, amount, "satoshi")]
    elif fee < 0.01:  # if the bot fee is less than 1 cent, don't take any fee
        outputs = [(recipient_address, sent_amount, "usd")]
    else:
        sent_amount -= fee  # deducts fee
        outputs = [
            (recipient_address, sent_amount, "usd"),
            (FEE_ADDRESS, fee, "usd"),
        ]

    try:
        key.send(outputs, fee=1)
    except Exception:
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text="Transaction failed!",
            parse_mode=ParseMode.MARKDOWN,
        )

    if satoshi:
        message = "You sent " + amount + " satoshis to " + recipient_username
    else:
        message = "You sent $" + amount + " to " + recipient_username
    return bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )


def price(bot, update, args):
    """ Fetches and returns the price of BCH (in USD) """
    currency = args[0].upper() if args else "USD"

    # fetches rate and rounds to appropriate decimal
    if currency == "BTC":
        bch_price = round(get_rate(update, currency), 4)
    else:
        bch_price = round(get_rate(update, currency))

    return bot.send_message(
        chat_id=update.effective_chat.id,
        text="1 BCH = " + str(bch_price) + " " + currency,
        parse_mode=ParseMode.MARKDOWN,
    )
