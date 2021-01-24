from typing import Union

from discord import Message, Embed
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
        data = self.tag_keeper.get(key)
        text = ''
        embed = None
        if isinstance(data, dict):
            embed = Embed.from_dict(data)
        else:
            text = data
        await ctx.send(text, embed=embed)

    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def create(self, ctx, key: str, *, value: Union[Message, str]):
        """
        Create a new tag.

        Args:
            key: Tag name. If it contains spaces, put it in quotes.
            value: Tag value.
        """
        if isinstance(value, Message):
            if len(value.embeds) > 0:
                value = value.embeds[0].to_dict()
            else:
                value = value.content
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
