import discord
from discord.ext.commands import UserInputError

from extensions.booksearch import handlers


class UnSupportedSite(UserInputError):
    pass


class BookSite:
    def __init__(self, ctx, handler):
        self.handler = handler(ctx.bot.loop)

    @classmethod
    async def convert(cls, ctx, argument):
        argument = argument.lower()
        handler = getattr(handlers, f'{argument.capitalize()}Handler', None)
        if handler is not None:
            return cls(ctx, handler)
        else:
            raise UnSupportedSite(f"{argument} is not a supported site!")

    async def search(self, query) -> discord.Embed:
        results, search_url = await self.handler.search(query)

        e = discord.Embed(title='Search Results', url=search_url)
        for result in results:
            title, subtext = self.handler.format_result(result)
            e.add_field(name=title, value=subtext, inline=False)

        return e

    @staticmethod
    def libraries():
        libraries = set()

        for name in handlers.__dict__:
            if name.endswith('Handler'):
                libraries.add(name.replace('Handler', '').lower())

        return libraries
