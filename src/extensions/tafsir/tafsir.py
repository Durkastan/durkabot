import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import BadArgument

from extensions.tafsir.handlers.altafsir import AlTafsir


class Tafsir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.handlers = [AlTafsir()]
        self.session = ClientSession(loop=bot.loop)

    @commands.command()
    async def tafsir(self, ctx, req, tafsir, language='en'):
        """Tafsir al Qur'an

        Args:
            req: The verse range in the format ss:i-j
            tafsir: The tafsir name.
            language(optional): The language of tafsir to return, in 2-letter format. e.g: en
        """
        handler = self.get_handler_with_support(tafsir, language)

        if not handler:
            raise BadArgument("Unsupported tafsir! Supported tafsirs are: ")

        url = handler.get_url(req, tafsir, language)
        response = await self.fetch(url)
        data = handler.parse(response)

        embed = self.make_embed(data, url, req)
        await ctx.send(embed=embed)

    async def fetch(self, url):
        async with self.session.get(url) as r:
            return await r.text()

    def get_handler_with_support(self, tafsir, language):
        for handler in self.handlers:
            if handler.is_supported(tafsir, language):
                return handler
        return None

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
