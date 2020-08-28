import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import BadArgument

from extensions.tafsir.handlers.altafsir import AlTafsir


class Tafsir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.handler = AlTafsir()
        self.session = ClientSession(loop=bot.loop)

    @commands.command()
    async def tafsir(self, ctx, req, tafsir, language='en'):
        if not self.handler.is_supported(tafsir, language):
            tafsirs = self.handler._tafsirs.keys()
            raise BadArgument("Invalid tafsir! Supported tafsirs are: " + tafsirs)

        url = self.handler.get_url(req, tafsir, language)
        response = await self.fetch(url)
        data = self.handler.parse(response)

        embed = self.make_embed(data, url, req)
        await ctx.send(embed=embed)

    async def fetch(self, url):
        async with self.session.get(url) as r:
            return await r.text()

    @staticmethod
    def make_embed(data, url, req):
        e = discord.Embed(title=data.tafsir_name + " | " + data.surah_name + " | " + req,
                          color=35810, description=f"[link]({url})\n\n" + data.ayah_text)
        txt = data.tafsir_text
        while len(txt) > 0 and not txt.isspace():
            ind = txt.rfind(' ', 700, 1000)
            part = txt[:ind]
            txt = txt[ind:]
            e.add_field(name='​', value=part, inline=False)  # that's a zero width space
        e.set_thumbnail(url="https://i.imgur.com/BOJeLJF.png")
        return e
