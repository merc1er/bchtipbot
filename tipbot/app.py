from telegram.ext import Updater, CommandHandler
from commands import *
from admin.commands import stats
import logging
import os
from settings import TOKEN, DEBUG
from db.models import db, User


if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Runs the bot"""
    db.connect()
    db.create_tables([User], safe=True)

    updater = Updater(TOKEN)

    # Commands
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler("deposit", deposit))
    updater.dispatcher.add_handler(CommandHandler("balance", balance))
    updater.dispatcher.add_handler(CommandHandler("withdraw", withdraw))
    updater.dispatcher.add_handler(CommandHandler("tip", tip))
    updater.dispatcher.add_handler(CommandHandler("price", price))
    # admin commands
    updater.dispatcher.add_handler(CommandHandler("stats", stats))

    if DEBUG:
        updater.start_polling()
    else:
        NAME = os.environ.get("NAME", "bchtipbot")
        # Start the webhook
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", "8443")),
            url_path=TOKEN,
            webhook_url="https://{}.herokuapp.com/{}".format(NAME, TOKEN),
        )

    updater.idle()


if __name__ == "__main__":
    main()
