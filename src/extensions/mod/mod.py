import discord
from discord.ext import commands


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, *members: discord.Member):
        """
        Swing your mighty Durkastani-made banhammer!

        Args:
            members: A list of users. Just mention!
        """
        for member in members:
            await ctx.guild.ban(member)
