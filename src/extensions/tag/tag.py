import pymongo
from discord.ext import commands

from storage import StorageHandler


class Tag:
    collection_name = 'tags'

    def __init__(self, bot):
        self.bot = bot
        self.storage = StorageHandler()
        self.collection = self.storage.db[self.collection_name]

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    async def tag(self, ctx, *, key):
        tag = self.collection.find_one({'key': key})
        await ctx.send(tag['value'])

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def create(self, ctx, key: str, *, value: str):
        self.collection.replace_one({'key': key}, {'key': key, 'value': value}, upsert=True)
        await ctx.send(f'Tag `{key}` created.')

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def delete(self, ctx, *, key):
        result = self.collection.delete_one({'key': key})
        if result.deleted_count != 0:
            await ctx.send(f'Tag `{key}` deleted.')
        else:
            await ctx.send(f'No tag `{key}`.')

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def list(self, ctx):
        cursor = self.collection.find(projection={'key': True})
        cursor.sort('key', pymongo.ASCENDING)
        tag_names = "\n".join([tag['key'] for tag in cursor])
        await ctx.send(f'```\n{tag_names}```')
