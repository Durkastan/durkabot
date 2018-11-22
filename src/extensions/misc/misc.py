from discord.ext import commands


class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['takbir'])
    async def takbeer(self, ctx):
        await ctx.send("Allahu Akbar!")
