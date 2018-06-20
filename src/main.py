import asyncio
import logging
import traceback
import os

from discord.ext import commands
from discord.ext.commands import UserInputError, MissingPermissions, BotMissingPermissions

from util import get_prefix


EXTENSIONS_DIR = "extensions"

DESCRIPTION = """DURKA DURKA"""


class Bot(commands.Bot):
    """Required environment variables are: DISCORD_TOKEN"""
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description=DESCRIPTION,
            loop=asyncio.new_event_loop(),
        )

    async def on_ready(self):
        print(self.user.name, ' : ', self.user.id)

        await self.change_presence(status='dnd')
        self._load_cogs()
        await self.change_presence(status='online')

    def _load_cogs(self):
        logging.info('Loading cogs...')
        for i in os.listdir(EXTENSIONS_DIR):
            extension_dir = os.path.join(EXTENSIONS_DIR, i)
            if os.path.isdir(extension_dir):
                if os.path.isfile(os.path.join(extension_dir, '__init__.py')):
                    try:
                        self.load_extension(f"{EXTENSIONS_DIR}.{i}")
                    except Exception:
                        logging.error(f'Error loading {i}: {traceback.format_exc()}')
        logging.info('Loaded.')

    async def on_command_error(self, ctx, exception):
        """Report an error if user uses command incorrectly, or in case of missing permissions."""
        if isinstance(exception, (MissingPermissions, BotMissingPermissions, UserInputError)):
            await ctx.send(str(exception))
        else:
            await super().on_command_error(ctx, exception)


def main():
    while True:
        try:
            Bot().run(os.environ.get('DISCORD_TOKEN'))
        except Exception:
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
