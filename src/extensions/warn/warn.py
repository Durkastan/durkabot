import discord
from discord.ext import commands
from discord.ext.commands import Cog

from common.permission import has_permissions
from extensions.warn.warner import Warner, AfterWarnAction


class Warn(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warner = None

        for guild in self.bot.guilds:
            self.bot.loop.create_task(Warner.periodically_forget_warns(guild.id))

    async def cog_before_invoke(self, ctx):
        self.warner = Warner(ctx.guild.id)

    @commands.command()
    @has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=""):
        """
        Warn a member

        Args:
            member: Just mention 'em, boss.
            reason(optional): For safekeeping.
        """
        action, num_warns = self.warner.warn(member, reason, ctx.channel.id, ctx.message.id, ctx.author.id)
        if action == AfterWarnAction.REPLY_KICK:
            await ctx.send("Warned too many times, eh? You get the boot. Good riddance.")
            await ctx.guild.kick(member)
        elif action == AfterWarnAction.REPLY:
            txt = f'{member.mention} You have been issued a warning'
            txt += (f' for the following: ```{reason}```' if reason else '.')
            txt += f" {num_warns}/3"
            await ctx.send(txt)

    @commands.command()
    @has_permissions(kick_members=True)
    async def warns(self, ctx, member: discord.Member):
        """
        Return a member's warn instances

        Args:
            member: Just mention 'em, boss.
        """
        await ctx.trigger_typing()
        doc = self.warner.get_raw_warns(member)

        if doc is None or doc['warns'] == []:
            await ctx.send(f"{member.mention} has no effective warns.")
            return

        warns = doc['warns']
        data = []
        for warn in warns:
            warn['by'] = (await self.bot.get_user_info(warn['by'])).mention
            link = (f"https://discordapp.com/channels/{getattr(ctx.guild, 'id','@me')}"
                    f"/{warn['channel_id']}/{warn['message_id']}")
            data.append((warn, link))

        await ctx.send(self.warner.format_warns(data))

    @commands.command()
    @has_permissions(kick_members=True)
    async def allwarns(self, ctx, member: discord.Member):
        """
        Return a member's warn instances, including old ones

        Args:
            member: Just mention 'em, boss.
        """
        await ctx.trigger_typing()
        doc = self.warner.get_raw_warns(member)

        if doc is None or (doc['warns'] == [] and doc['previous_warns'] == []):
            await ctx.send(f"{member.mention} has no warns.")
            return

        for warn in doc['previous_warns']:
            warn['tag'] = '(non-effective)'

        warns = doc['previous_warns'] + doc['warns']
        data = []

        for warn in warns:
            warn['by'] = (await self.bot.get_user_info(warn['by'])).mention
            link = (f"https://discordapp.com/channels/{getattr(ctx.guild, 'id', '@me')}"
                    f"/{warn['channel_id']}/{warn['message_id']}")
            data.append((warn, link))

        await ctx.send(self.warner.format_warns(data))
