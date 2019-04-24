import discord
from discord.ext import commands
from discord.ext.commands import Cog

from extensions.meme.psst import format_psst


class Meme(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def psst(self, ctx, *, txt: str):
        """hey kid!"""
        processed = format_psst(discord.utils.escape_mentions(txt))
        await ctx.send(processed)


