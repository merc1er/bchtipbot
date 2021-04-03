import os


# Define settings
try:
    DEBUG = os.environ["DEBUG"] == "True"  # because DEBUG is a string
except KeyError:
    DEBUG = True


try:
    TOKEN = os.environ["TOKEN"]
except KeyError:
    # This Token is for the test bot.
    # It is recommended that you create your own bot for testing and create the
    # TOKEN environment variable.
    # I will still leave my test token here for quick testing.
    TOKEN = "892772409:AAGQk_Fyz3Uelwvhoq8yUmRXPUuTxnFFIfY"


# Your output BCH address
FEE_ADDRESS = "bitcoincash:qrp4rsv05s5stsec8z7q8hjujvhnggf4scqpu2ezme"
# The fee you want to charge (0.01 is 1%)
FEE_PERCENTAGE = 0.01


# List of administrators allowed to use the admin commands
ADMIN_LIST = [
    "merc1er",
]
