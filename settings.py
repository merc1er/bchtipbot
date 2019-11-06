import os


# Define settings
try:
    DEBUG = os.environ['DEBUG'] == 'True'  # because DEBUG is a string
except:
    DEBUG = True


try:
    TOKEN = os.environ['TOKEN']
except:
    TOKEN = '892772409:AAGQk_Fyz3Uelwvhoq8yUmRXPUuTxnFFIfY'


DATABASE_PINK = 'db.sqlite3'

# Your output BCH address
try:
    FEE_ADDRESS = os.environ['FEE_ADDRESS']
except:
    FEE_ADDRESS = 'bitcoincash:qr02vc2t5yr9fe4ujdpkg99d5d0dgxstfqtgxg7umu'
# The fee you want to charge (0.01 is 1%)
FEE_PERCENTAGE = 0.01
