from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog, has_permissions

from common.converters import from_json


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['takbir'])
    async def takbeer(self, ctx):
        """
        Allahu Akbar!
        """
        await ctx.send("Allahu Akbar!")

    @commands.command()
    @has_permissions(manage_messages=True)
    async def embed(self, ctx, *, data: from_json):
        """
        Create an embed using a json object

        https://leovoel.github.io/embed-visualizer/ is a useful resource for designing embeds.

        Note that one should only supply the bot with the value of the field `embed`, and not
        the whole thing that website throws out.
        """
        e = Embed.from_dict(data)
        await ctx.send(embed=e)
