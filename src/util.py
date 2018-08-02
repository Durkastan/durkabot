import os


def get_prefix(bot, message):
    """TODO: Dynamic prefix for each server"""
    return os.environ.get('PREFIX', "durka ")
