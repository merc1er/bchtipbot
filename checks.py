

def amount_is_valid(amount):
    """ Checks if [amount] is a valid BCH amount """
    try:
        amount = float(amount)
        if amount < 0.00000001 or amount > 21000000:
            return False
    except:
        return False

    return True
