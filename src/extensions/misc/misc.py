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
        """
        if data.get("embed"):
            data = data['embed']
        e = Embed.from_dict(data)
        await ctx.send(embed=e)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
