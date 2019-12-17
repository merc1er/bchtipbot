# Functions checking for incorrect inputs


def check_username(update):
    """
    Checks for username.
    Returns True if user has a uname set up, False otherwise
    """
    if not update.message.from_user.username:
        update.message.reply_text('You do not have a username. Please create '
                                  'one in settings to use this bot.')
        return False
    return True


def amount_is_valid(amount):
    """ Checks if [amount] is a valid BCH amount """
    try:
        amount = float(amount)
        if amount <= 0:
            return False
    except Exception:
        return False

    return True


def username_is_valid(username):
    """ Checks if a Telegram username is valid """
    if username[0] != '@':
        return False
    username = username[1:]  # remove the '@'
    if len(username) < 5 or len(username) > 30:
        return False
    # TODO: check for special characters
    return True
