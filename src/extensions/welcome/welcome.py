from discord.ext.commands import Cog

welcome_channel_id = 458493647609004035

welcome_message = (
    "Welcome -- please make sure to read "
    "<#458932170267033603>  <#458500334973616129>  <#487013175963811851> ... "
    "If you have any questions please ask in one of the free discussion channels, "
    "someone will see to your question soon, "
    "feel free to look around and engage in the various channels here to learn or contribute. "
    "{}"
)


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener
    async def on_member_update(self, before, after):
        if len(before.roles) == 1 and len(after.roles) > 1:
            welcome_channel = after.guild.get_channel(welcome_channel_id)
            await welcome_channel.send(welcome_message.format(after.mention))
