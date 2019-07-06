from discord.ext.commands import Cog

from storage import StorageHandler


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_update(self, before, after):
        config = StorageHandler.config(before.guild.id)
        if config["welcome_channel_id"] is None or config['welcome_message'] is None:
            return
        if len(before.roles) == 1 and len(after.roles) > 1:
            welcome_channel = after.guild.get_channel(config["welcome_channel_id"])
            welcome_message = config['welcome_message']
            await welcome_channel.send(welcome_message.format(after.mention))
