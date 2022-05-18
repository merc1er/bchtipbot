from db.get import count_users
from settings import ADMIN_LIST


def is_admin(command):
    """Decorator to check if sender is admin"""
    # check if admin here

    def wrapper(*args, **kwargs):
        if args[1].message.from_user.username in ADMIN_LIST:
            return command(*args, **kwargs)
        else:
            return False

    return wrapper


@is_admin
def stats(bot, update):
    return update.message.reply_text("Users: " + str(count_users()))
