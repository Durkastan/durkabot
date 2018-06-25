from discord.ext import commands

from extensions.booksearch.booksite import BookSite


class BookSearch:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def booksearch(self, ctx, book_site: BookSite, query: str, tag: str = None):
        embed = await book_site.search(query, tag)
        await ctx.send(embed=embed)
