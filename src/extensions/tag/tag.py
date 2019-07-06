from discord.ext import commands
from discord.ext.commands import Cog

from extensions.tag.tag_keeper import TagKeeper


class Tag(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tag_keeper = None

    async def cog_before_invoke(self, ctx):
        self.tag_keeper = TagKeeper(ctx.guild.id)

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, key):
        """
        Return text stored under tag.

        Args:
            key: Tag name. See the "tag list" subcommand
        """
        await ctx.send(self.tag_keeper.get(key))

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def create(self, ctx, key: str, *, value: str):
        """
        Create a new tag.

        Args:
            key: Tag name. If it contains spaces, put it in quotes.
            value: Tag value.
        """
        self.tag_keeper.create(key, value)
        await ctx.send(f'Tag `{key}` created.')

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def delete(self, ctx, *, key):
        """
        Delete a tag.

        Args:
            key: Tag name.
        """
        was_deleted = self.tag_keeper.delete(key)
        if was_deleted:
            await ctx.send(f'Tag `{key}` deleted.')
        else:
            await ctx.send(f'No tag `{key}`.')

    @tag.command()
    async def list(self, ctx):
        """
        List stored tags.
        """
        await ctx.send(f'```\n{self.tag_keeper.list()}```')
