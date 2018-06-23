from discord.ext import commands

from extensions.booksearch.booksite import BookSite


class BookSearch:
    @commands.command()
    async def booksearch(self, ctx, book_site: BookSite, query: str, tags: str = None):
        pass
