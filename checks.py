# Functions checking for incorrect inputs


def amount_is_valid(amount):
    """ Checks if [amount] is a valid BCH amount """
    try:
        amount = float(amount)
        if amount <= 0 or amount > 2100000000000000:
            # minimum is 1 satoshi, maximum 21M BCH
            return False
    except:
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
