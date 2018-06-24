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

    async def search(self, query, tag) -> discord.Embed:
        results, search_url = await self.handler.search(query, tag)

        e = discord.Embed(title='Search Results', url=search_url)
        for result in results:
            value = (f"by {result.author_name}\n"
                     + (f"[Link on archive.org]({result.link}), " if result.link is not None else '')
                     + (f"[link on waqfeya.com]({result.site_link})" if result.site_link is not None else ''))
            e.add_field(name=result.title, value=value)

        return e
