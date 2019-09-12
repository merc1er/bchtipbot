import os


# Define settings
try:
    DEBUG = os.environ['DEBUG'] == 'True'  # because DEBUG is a string
except:
    DEBUG = True


DATABASE_PINK = 'db.sqlite3'
TOKEN = '892772409:AAGQk_Fyz3Uelwvhoq8yUmRXPUuTxnFFIfY'

