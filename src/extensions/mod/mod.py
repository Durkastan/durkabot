import discord
from discord.ext import commands
from discord.ext.commands import Cog

from common.permission import has_permissions


class Mod(Cog):
    dm_template = """You have been {0} from {1}"""
    reason_snippet = " for: {0}"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = ''):
        """
        Swing your mighty Durkastani-made banhammer!

        Args:
            member: Your lucky user. Just mention!
            reason(optional):
        """
        dm = self.dm_template.format("banned", ctx.guild.name)
        if reason:
            dm += self.reason_snippet.format(reason)
        await member.send(dm)
        await ctx.guild.ban(member, reason=reason)
        await ctx.send("Banned.", delete_after=5)

    @commands.command()
    @has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = ''):
        """
        Polish your boot for this one.

        Args:
            member: Your lucky user. Just mention!
            reason(optional):
        """
        dm = self.dm_template.format("kicked", ctx.guild.name)
        if reason:
            dm += self.reason_snippet.format(reason)
        await member.send(dm)
        await ctx.guild.kick(member, reason=reason)
        await ctx.send('Booted.', delete_after=5)

    @commands.command()
    @has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 100, *members: discord.Member):
        """
        DELET

        Args:
            limit: The number of messages to search through.
            *members: If supplied, only messages from those users will
                    be deleted. Otherwise, all messages are fair game.
        """
        check = (lambda m: m.author in members) if members else None
        await ctx.channel.purge(limit=limit, check=check)

    @commands.command()
    @has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, *, role_name):
        """
        Add/remove a role to the given member
        Args:
            member: The member to add the role to
            role_name: Role name, case-insensitive
        """
        role = discord.utils.find(lambda r: r.name.lower() == role_name, member.guild.roles)
        if role not in member.roles:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)

    async def cog_after_invoke(self, ctx):
        await ctx.message.delete()
