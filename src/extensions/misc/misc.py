from discord.ext import commands
from discord.ext.commands import Cog


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['takbir'])
    async def takbeer(self, ctx):
        """
        Allahu Akbar!
        """
        await ctx.send("Allahu Akbar!")
