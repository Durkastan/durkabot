import discord
from discord.ext import commands

from common.permission import has_permissions


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, *members: discord.Member):
        """
        Swing your mighty Durkastani-made banhammer!

        Args:
            members: A list of users. Just mention!
        """
        if members:
            for member in members:
                await ctx.guild.ban(member)
            await ctx.send("Banned.")
        else:
            await ctx.send("Whaddaya mean, 'just ban anyone?'")

    @commands.command()
    @has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, *members: discord.Member):
        """
        Polish your boot for this one.

        Args:
            members: A list of users. Just mention!
        """
        if members:
            for member in members:
                await ctx.guild.kick(member)
            await ctx.send('Booted.')
        else:
            await ctx.send("Sorry chief, can't boot.")

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
        Add a role to the given member
        Args:
            member: The member to add the role to
            role_name: Role name, case-insensitive
        """
        role = discord.utils.find(lambda r: r.name.lower() == role_name, member.guild.roles)
        await member.add_roles(role)
