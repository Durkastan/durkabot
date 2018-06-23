from discord.ext.commands import UserInputError

from extensions.booksearch import handlers


class UnSupportedSite(UserInputError):
    pass


class BookSite:
    supported_sites = {
        'waqfeya': 'waqfeya.com'
    }

    def __init__(self, ctx, handler):
        self.ctx = ctx
        self.handler = handler(ctx)

    @classmethod
    async def convert(cls, ctx, argument):
        argument = argument.lower()
        if argument in cls.supported_sites:
            return cls(ctx, getattr(handlers, f'{argument.capitalize()}Handler'))
        else:
            raise UnSupportedSite(f"{argument} is not a supported site!")
