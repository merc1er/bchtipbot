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
    """ Runs the bot """
    db.connect()
    db.create_tables([User], safe=True)

    updater = Updater(TOKEN)

    # Commands
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler("deposit", deposit))
    updater.dispatcher.add_handler(
        CommandHandler("balance", balance, pass_args=True)
    )
    updater.dispatcher.add_handler(
        CommandHandler("withdraw", withdraw, pass_args=True)
    )
    updater.dispatcher.add_handler(CommandHandler("tip", tip, pass_args=True))
    updater.dispatcher.add_handler(
        CommandHandler("price", price, pass_args=True)
    )
    # admin commands
    updater.dispatcher.add_handler(CommandHandler("stats", stats))
    # Playmo commands
    updater.dispatcher.add_handler(
        CommandHandler("playmo", playmo_get_game_overview, pass_args=True)
    )

    if DEBUG:
        updater.start_polling()
    else:
        # Port is given by Heroku
        PORT = os.environ.get("PORT")
        try:
            NAME = os.environ.get("NAME")
        except KeyError:
            NAME = "bchtipbot"
        # Start the webhook
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
        updater.bot.setWebhook(
            "https://{}.herokuapp.com/{}".format(NAME, TOKEN)
        )

    updater.idle()


if __name__ == "__main__":
    main()
