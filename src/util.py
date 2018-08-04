import os

def get_prefix(bot, message):
    """TODO: Dynamic prefix for each server"""
    prefix_list = ['d ', 'D ', 'durka ', 'Durka ']

    return os.environ.get('PREFIX', prefix_list)
