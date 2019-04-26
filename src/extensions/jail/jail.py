import discord
from discord.ext.commands import Cog

from extensions.jail.jailer import Jailer


class Jail(Cog):
    JAIL_ROLE_ID = 459467057151475716

    def __init__(self, bot):
        self.bot = bot
        self.jailer = Jailer()

    async def jail(self, ctx, *members: discord.Member):
        jail_role = ctx.guild.get_role(self.JAIL_ROLE_ID)

        for member in members:
            old_roles = member.roles
            self.jailer.jail(member)

            await member.add_roles(jail_role)
            await member.remove_roles(old_roles)

    async def unjail(self, ctx, *members: discord.Member):
        jail_role = ctx.guild.get_role(self.JAIL_ROLE_ID)

        for member in members:
            ctx.guild.get_role()
            role_ids = self.jailer.unjail(member)
            roles = [ctx.guild.get_role(role_id) for role_id in role_ids]

            await member.add_roles(roles)
            await member.remove_roles(jail_role)
