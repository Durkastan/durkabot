from discord.ext import commands

from extensions.meme.psst import format_psst


class Meme:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def psst(self, ctx, *, txt: str):
        """hey kid!"""
        processed = format_psst(txt)
        await ctx.send(processed)


