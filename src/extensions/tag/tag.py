from discord.ext import commands

from storage import StorageHandler


class Tag:
    db = 'tags'

    def __init__(self, bot):
        self.bot = bot
        self.storage = StorageHandler()

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, key):
        self.storage.feed(ctx)
        tag = self.storage.db[self.db].find_one({'key': key})
        await ctx.send(tag['value'])

    @tag.command()
    async def add(self, ctx, key: str, value: str):
        self.storage.feed(ctx)
        self.storage.db[self.db].replace_one({'key': key}, {'key': key, 'value': value}, upsert=True)
        await ctx.send(f'Tag {key} created.')
