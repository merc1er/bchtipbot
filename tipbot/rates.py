import requests


RATE_API = "https://bitpay.com/rates/BCH/"
CURRENCY_CODE = {
    "BTC": 0,
    "BCH": 1,
    "USD": 2,
    "EUR": 3,
    "GBP": 4,
    "JPY": 5,
    "CAD": 6,
    "AUD": 7,
    "CNY": 8,
    "CHF": 9,
    "SEK": 10,
    "NZD": 11,
    "KRW": 12,
    "ETH": 13,
    "XRP": 14,
    "AED": 15,
    "AFN": 16,
    "ALL": 17,
    "AMD": 18,
    "ANG": 19,
    "AOA": 20,
    "ARS": 21,
    "AWG": 22,
    "AZN": 23,
    "BAM": 24,
    "BBD": 25,
    "BDT": 26,
    "BGN": 27,
    "BHD": 28,
    "BIF": 29,
    "BMD": 30,
    "BND": 31,
    "BOB": 32,
    "BRL": 33,
    "BSD": 34,
    "BTN": 35,
    "BUSD": 36,
    "BWP": 37,
    "BYN": 38,
    "BZD": 39,
    "CDF": 40,
    "CLF": 41,
    "CLP": 42,
    "COP": 43,
    "CRC": 44,
    "CUP": 45,
    "CVE": 46,
    "CZK": 47,
    "DJF": 48,
    "DKK": 49,
    "DOP": 50,
    "DZD": 51,
    "EGP": 52,
    "ETB": 53,
    "FJD": 54,
    "FKP": 55,
    "GEL": 56,
    "GHS": 57,
    "GIP": 58,
    "GMD": 59,
    "GNF": 60,
    "GTQ": 61,
    "GUSD": 62,
    "GYD": 63,
    "HKD": 64,
    "HNL": 65,
    "HRK": 66,
    "HTG": 67,
    "HUF": 68,
    "IDR": 69,
    "ILS": 70,
    "INR": 71,
    "IQD": 72,
    "IRR": 73,
    "ISK": 74,
    "JEP": 75,
    "JMD": 76,
    "JOD": 77,
    "KES": 78,
    "KGS": 79,
    "KHR": 80,
    "KMF": 81,
    "KPW": 82,
    "KWD": 83,
    "KYD": 84,
    "KZT": 85,
    "LAK": 86,
    "LBP": 87,
    "LKR": 88,
    "LRD": 89,
    "LSL": 90,
    "LYD": 91,
    "MAD": 92,
    "MDL": 93,
    "MGA": 94,
    "MKD": 95,
    "MMK": 96,
    "MNT": 97,
    "MOP": 98,
    "MRU": 99,
    "MUR": 100,
    "MVR": 101,
    "MWK": 102,
    "MXN": 103,
    "MYR": 104,
    "MZN": 105,
    "NAD": 106,
    "NGN": 107,
    "NIO": 108,
    "NOK": 109,
    "NPR": 110,
    "OMR": 111,
    "PAB": 112,
    "PAX": 113,
    "PEN": 114,
    "PGK": 115,
    "PHP": 116,
    "PKR": 117,
    "PLN": 118,
    "PYG": 119,
    "QAR": 120,
    "RON": 121,
    "RSD": 122,
    "RUB": 123,
    "RWF": 124,
    "SAR": 125,
    "SBD": 126,
    "SCR": 127,
    "SDG": 128,
    "SGD": 129,
    "SHP": 130,
    "SLL": 131,
    "SOS": 132,
    "SRD": 133,
    "STN": 134,
    "SVC": 135,
    "SYP": 136,
    "SZL": 137,
    "THB": 138,
    "TJS": 139,
    "TMT": 140,
    "TND": 141,
    "TOP": 142,
    "TRY": 143,
    "TTD": 144,
    "TWD": 145,
    "TZS": 146,
    "UAH": 147,
    "UGX": 148,
    "USDC": 149,
    "UYU": 150,
    "UZS": 151,
    "VEF": 152,
    "VES": 153,
    "VND": 154,
    "VUV": 155,
    "WST": 156,
    "XAF": 157,
    "XAG": 158,
    "XAU": 159,
    "XCD": 160,
    "XPF": 161,
    "XOF": 162,
    "YER": 163,
    "ZAR": 164,
    "ZMW": 165,
    "ZWL": 166,
}


def get_rate(update, currency="USD"):
    """Returns the BCH price fetching BitPay API

    API documentation:
    https://bitpay.com/api/#rest-api-resources-rates-fetch-the-rates-used-by-bitpay-for-a-specific-cryptocurrency
    """
    currency = currency.upper()

    if currency not in CURRENCY_CODE:
        return update.message.reply_text(f"{currency} is not a supported " "currency.")

    r = requests.get(RATE_API)
    if r.status_code != 200:  # pragma: no cover
        return update.message.reply_text(f"Unable to contact {RATE_API}")

    data = r.json()["data"]
    rate = data[CURRENCY_CODE[currency]]["rate"]

    return rate
