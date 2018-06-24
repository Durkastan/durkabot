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
            value = (f"لـ {result.author_name}\n"
                     + (f"[---]({result.link}) :الرابط على موقع ارشيف\n" if result.link is not None else '')
                     + (f"[---]({result.site_link}) :الرابط على موقع وقفية\n" if result.site_link is not None else ''))
            e.add_field(name=result.title, value=value, inline=False)

        return e
