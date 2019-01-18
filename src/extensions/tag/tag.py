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
    async def tag(self, ctx, *, key):
        """
        Return text stored under tag.

        Args:
            key: Tag name. See the "tag list" subcommand
        """
        tag = self.collection.find_one({'key': key})
        await ctx.send(tag['value'])

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def create(self, ctx, key: str, *, value: str):
        """
        Create a new tag.

        Args:
            key: Tag name. If it contains spaces, put it in quotes.
            value: Tag value.
        """
        self.collection.replace_one({'key': key}, {'key': key, 'value': value}, upsert=True)
        await ctx.send(f'Tag `{key}` created.')

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def delete(self, ctx, *, key):
        """
        Delete a tag.

        Args:
            key: Tag name.
        """
        result = self.collection.delete_one({'key': key})
        if result.deleted_count != 0:
            await ctx.send(f'Tag `{key}` deleted.')
        else:
            await ctx.send(f'No tag `{key}`.')

    @tag.command()
    async def list(self, ctx):
        """
        List stored tags.
        """
        cursor = self.collection.find(projection={'key': True})
        cursor.sort('key', pymongo.ASCENDING)
        tag_names = "\n".join([tag['key'] for tag in cursor])
        await ctx.send(f'```\n{tag_names}```')
