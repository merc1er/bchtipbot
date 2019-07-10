from telegram.ext import Updater, CommandHandler
from db.init import init_database
from commands import *
import logging
from settings import TELEGRAM_TOKEN


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    """ Runs the bot
    """
    init_database()
    updater = Updater(TELEGRAM_TOKEN)

    # Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('deposit', deposit))
    updater.dispatcher.add_handler(CommandHandler('balance', balance))
    updater.dispatcher.add_handler(CommandHandler('withdraw',
                                                    withdraw, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('tip', tip, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('add_funds', add_funds))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
