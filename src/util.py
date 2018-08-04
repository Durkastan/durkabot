import os

def get_prefix(bot, message):
    """TODO: Dynamic prefix for each server"""
    return [
            'd ',
            'D ',
            'durka ',
            'Durka ',
            os.environ.get('PREFIX')
    ]
