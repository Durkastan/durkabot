from discord.ext import commands

from storage import StorageHandler


class Tag:
    collection = 'tags'

    def __init__(self, bot):
        self.bot = bot
        self.storage = StorageHandler()

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    async def tag(self, ctx, key):
        tag = self.storage.db[self.collection].find_one({'key': key})
        await ctx.send(tag['value'])

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def create(self, ctx, key: str, *, value: str):
        self.storage.db[self.collection].replace_one({'key': key}, {'key': key, 'value': value}, upsert=True)
        await ctx.send(f'Tag {key} created.')
