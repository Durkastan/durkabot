import discord
from discord.ext.commands import Cog

from extensions.jail.jailer import Jailer


class Jail(Cog):
    JAIL_ROLE_ID = 0

    def __init__(self, bot):
        self.bot = bot
        self.jailer = Jailer()

    async def jail(self, ctx, *members: discord.Member):
        for member in members:
            await self.jailer.jail(member, discord.utils.get(ctx.guild.roles, id=self.JAIL_ROLE_ID))

    async def unjail(self, ctx, *members: discord.Member):
        for member in members:
            await self.jailer.unjail(member, discord.utils.get(ctx.guild.roles, id=self.JAIL_ROLE_ID))
