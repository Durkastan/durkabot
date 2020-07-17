# Suggestions cog, taken from https://github.com/TS96/MG-Bot with modifications
# MIT license

import discord
import datetime
from datetime import datetime
from dateutil import parser
from discord.ext import commands

from common.permission import has_permissions
from extensions.suggestions.suggestor import Suggestor

botlog_chat_id = 458507846049464330
suggestions_chat_id = 733761194971758663
default_suggestion_wait = 1
guild_id = 458493647609004033


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggestor = None

    async def cog_before_invoke(self, ctx):
        self.suggestor = Suggestor(ctx.guild.id)

    @has_permissions(kick_members=True)
    @commands.command(name="bansuggestions", help="ban user from making suggestions")
    async def ban_suggestions(self, ctx, member: discord.Member):
        self.suggestor.ban_suggestions_from(member.id)
        await ctx.channel.send("Member banned from making suggestions")

    @has_permissions(kick_members=True)
    @commands.command(name="unbansuggestions", help="unban user from making suggestions")
    async def unban_suggestions(self, ctx, member: discord.Member):
        self.suggestor.unban_suggestions_from(member.id)
        await ctx.channel.send("Member can make suggestions again")

    @has_permissions(kick_members=True)
    @commands.command(name="suggestion", help="prints suggestion info in #bot_log")
    async def get_suggestion(self, ctx, message_id):
        suggestion = self.suggestor.get_suggestion(message_id)
        if suggestion is None:
            await ctx.guild.get_channel(botlog_chat_id).send("Suggestion not found")
            return

        member = ctx.guild.get_member(int(suggestion['user_id']))

        embed = discord.Embed(
            description=suggestion['suggestions'].strip(),
            timestamp=parser.parse(suggestion['date']), color=discord.Color.darker_grey())
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text="Suggestion ID: " + message_id)
        embed.set_thumbnail(url=member.avatar_url)

        await ctx.guild.get_channel(botlog_chat_id).send(embed=embed)

    @has_permissions(kick_members=True)
    @commands.command(name="suggestions", help="prints all suggestions by specified user in #bot_log")
    async def get_suggestions(self, ctx, member: discord.Member):
        msgs = []
        try:
            suggestions = self.suggestor.get_suggestions_from_user(member.id)
            current = "```User: " + member.name + "```\n\n"
            for item in suggestions:
                addition = "```Date: " + item['date'] + "\n" + item['suggestions'].strip() + "```\n\n"
                if len(current + addition) >= 2000:
                    msgs.append(current)
                    current = ""
                current += addition
            msgs.append(current)
            for item in msgs:
                await ctx.guild.get_channel(botlog_chat_id).send(item)
        except Exception as e:
            print(str(e))
            await ctx.channel.send("Invalid Command")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and message.content.lower().startswith('suggestion: '):
            await self.new_suggestion(message)

    async def new_suggestion(self, message):
        date = datetime.now()
        self.suggestor = Suggestor(guild_id)
        if self.suggestor.is_suggestion_banned(message.author.id):
            await message.author.send("You've been banned from making suggestions :(")
            return

        latest_sugg = self.suggestor.get_latest_suggestion_from_user(message.author.id)
        if latest_sugg is not None:
            date_delta = abs(date - latest_sugg['date'])
            if date_delta.days <= 0 and date_delta.seconds / 3600 < default_suggestion_wait:
                await message.author.send(
                    "Too soon! You need to wait " + str(
                        default_suggestion_wait * 60 - int(date_delta.seconds / 60)) + " minutes.")
                return
        embed = discord.Embed(
            description=message.content[message.content.find(' '):],
            timestamp=datetime.utcnow(), color=discord.Color.light_grey())
        embed.set_author(name="New Suggestion", icon_url=self.bot.get_guild(guild_id).icon_url)
        msg = await self.bot.get_channel(suggestions_chat_id).send(embed=embed)
        self.suggestor.add_new_suggestion(message, date, msg.id)
        await message.author.send("Thanks for your suggestion!")
