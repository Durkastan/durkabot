import json

from discord.ext.commands import BadArgument


def from_json(argument):
    try:
        return json.loads(argument.strip('`'))
    except Exception:
        raise BadArgument("Incorrect json string!")
