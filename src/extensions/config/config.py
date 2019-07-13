from discord.ext import commands
from discord.ext.commands import Cog, has_permissions

from static import DEFAULT_CONFIG


class Config(Cog):
    @commands.command()
    @has_permissions(kick_members=True)
    async def config(self, ctx, key: str, value=None):
        if key not in DEFAULT_CONFIG:
            await ctx.send(f"Invalid option! valid options are `{list(DEFAULT_CONFIG.keys())}`")
            return

        if value is None:
            # get
            await ctx.send(f"{key} is set to {ctx.config[key]}")
            return

        # set
        if type(value) != type(DEFAULT_CONFIG[key]):
            await ctx.send(f"{key} can only accept a value of type {type(DEFAULT_CONFIG[key])}")
            return
        doc = ctx.config
        doc[key] = type(DEFAULT_CONFIG[key])(value)
        ctx.write_config(ctx.guild.id, doc)

        await ctx.send(f"{key} set to {value}")
