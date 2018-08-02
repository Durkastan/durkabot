from discord.ext import commands

from extensions.archive.archive_handler import ArchiveHandler


class Archive:
    def __init__(self, bot):
        self.handler = ArchiveHandler(bot.loop)

    @commands.command()
    async def archive(self, ctx, link):
        result = await self.handler.archive(link)
        await ctx.send(result.link)
