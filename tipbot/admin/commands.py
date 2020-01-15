from db.get import count_users


def is_admin(command):
    """ Decorator to check if sender is admin """
    # check if admin here

    def wrapper(*args, **kwargs):
        return command(*args, **kwargs)
    return wrapper


@is_admin
def stats(bot, update):
    return update.message.reply_text('Users: ' + str(count_users()))
