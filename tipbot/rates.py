import requests


RATE_API = 'https://www.bitcoin.com/special/rates.json'
CURRENCY_CODE = {
    'usd': 2,
    'eur': 3,
    'gbp': 4,
    'jpy': 5,
    'cad': 6,
    'aud': 7,
    'cny': 8,
    'chf': 9,
    'sek': 10,
    'nzd': 11,
    'krw': 12,
    'thb': 137,
}


def get_rate(update, currency='usd'):
    """ Returns the BCH price fetching Bitcoin.com API """
    if currency not in CURRENCY_CODE:
        return update.message.reply_text(f'{currency} is not a supported '
                                         'currency.')
    r = requests.get(RATE_API)
    if r.status_code != 200:
        return update.message.reply_text(f'Unable to contact {RATE_API}')
    data = r.json()
    # Note: data[1]['rate'] is BTC/BCH ratio
    return data[CURRENCY_CODE[currency]]['rate'] / data[1]['rate']
