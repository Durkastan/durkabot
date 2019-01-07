import asyncio
import logging
import traceback
import os

from discord.ext import commands
from discord.ext.commands import UserInputError, MissingPermissions, BotMissingPermissions

from static import EXTENSIONS_DIR, DESCRIPTION
from storage import StorageHandler
from util import get_prefix


logger = logging.getLogger('durkabot')

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Bot(commands.Bot):
    """Required environment variables are: DISCORD_TOKEN"""
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description=DESCRIPTION,
            loop=asyncio.new_event_loop(),
        )

        self.logger = logger
        self.storage = StorageHandler

    async def on_ready(self):
        print(self.user.name, ' : ', self.user.id)

        await self.change_presence(status='dnd')
        self._load_cogs()
        await self.change_presence(status='online')

    def _load_cogs(self):
        self.logger.info('Loading cogs...')
        for i in os.listdir(EXTENSIONS_DIR):
            extension_dir = os.path.join(EXTENSIONS_DIR, i)
            if os.path.isdir(extension_dir):
                if os.path.isfile(os.path.join(extension_dir, '__init__.py')):
                    try:
                        self.load_extension(f"{os.path.basename(EXTENSIONS_DIR)}.{i}")
                    except Exception:
                        self.logger.error(f'Error loading {i}: {traceback.format_exc()}')
        self.logger.info('Loaded.')

    async def on_command_error(self, ctx, exception):
        """Report an error if user uses command incorrectly, or in case of missing permissions."""
        if isinstance(exception, (MissingPermissions, BotMissingPermissions, UserInputError)):
            await ctx.send(str(exception), delete_after=5)
        else:
            await super().on_command_error(ctx, exception)


def main():
    while True:
        try:
            Bot().run(os.environ.get('DISCORD_TOKEN'))
        except Exception:
            logger.critical(traceback.format_exc())


if __name__ == '__main__':
    main()
