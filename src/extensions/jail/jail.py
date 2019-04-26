import discord
from discord.ext import commands
from discord.ext.commands import Cog

from common.permission import has_permissions
from extensions.jail.jailer import Jailer


class Jail(Cog):
    JAIL_ROLE_ID = 459467057151475716

    def __init__(self, bot):
        self.bot = bot
        self.jailer = Jailer()

    @commands.command()
    @has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def jail(self, ctx, *members: discord.Member):
        jail_role = ctx.guild.get_role(self.JAIL_ROLE_ID)

        for member in members:
            old_roles = member.roles
            old_roles.remove(ctx.guild.default_role)
            self.jailer.jail(member, old_roles)

            await member.add_roles(jail_role)
            if old_roles:
                await member.remove_roles(*old_roles)

    @commands.command()
    @has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unjail(self, ctx, *members: discord.Member):
        jail_role = ctx.guild.get_role(self.JAIL_ROLE_ID)

        for member in members:
            role_ids = self.jailer.unjail(member)
            roles = [ctx.guild.get_role(role_id) for role_id in role_ids]

            if roles:
                await member.add_roles(*roles)
            await member.remove_roles(jail_role)
