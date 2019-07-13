from discord.ext import commands

from static import DEFAULT_CONFIG
from storage import StorageHandler


class ConfigContext(commands.Context):
    @property
    def config(self):
        if self.guild is None:
            return DEFAULT_CONFIG
        return StorageHandler.config(self.guild.id)

    def write_config(self, doc):
        if self.guild is None:
            return
        StorageHandler.write_config(self.guild.id, doc)
