from typing import List

import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands import BadArgument

from extensions.tafsir.handlers.alim import Alim
from extensions.tafsir.handlers.altafsir import AlTafsir
from extensions.tafsir.tafsir_handler import TafsirHandler, TafsirData


class Tafsir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.handlers: List[TafsirHandler] = [AlTafsir(), Alim()]
        self.session = ClientSession(loop=bot.loop)

    @commands.command()
    async def tafsir(self, ctx, req, tafsir=None, language=None):
        """Tafsir Al-Qur'an

        Args:
            req: The verse range in the format i:j
            tafsir: The tafsir name.
            language(optional): The language of tafsir to return, in 2-letter format. e.g: en
        """
        if tafsir is None and language is None:
            tafsir = "jalalayn"
            language = 'en'

        elif tafsir not in self.supported_tafsirs():
            raise BadArgument(f"Unsupported tafsir! Supported tafsirs are: `{', '.join(self.supported_tafsirs())}`")

        notes = ''

        if language is None:
            language = self.get_default_language_for(tafsir)

        elif language not in self.supported_languages_for(tafsir):
            languages = self.supported_languages_for(tafsir)

            notes += f"{tafsir} unavailable in `{language}`; fetching in `{languages[0]}`."
            if len(languages) > 1:
                notes += f" Also available in `{', '.join(languages[1:])}`"
            notes += "\n"

            language = languages[0]

        handler = self.get_handler_with_support(tafsir, language)

        url = handler.get_url(req, tafsir, language)
        response = await self.fetch(url)
        data = handler.parse(response)

        embed = self.make_embed(data, url, req)
        await ctx.send(notes, embed=embed)

    async def fetch(self, url):
        async with self.session.get(url) as r:
            return await r.text()

    def get_handler_with_support(self, tafsir, language):
        for handler in self.handlers:
            if handler.is_supported(tafsir, language):
                return handler
        return None

    def supported_tafsirs(self):
        supported: set = set()
        for handler in self.handlers:
            supported = supported.union(handler.tafsirs())
        return supported

    def supported_languages(self):
        supported: set = set()
        for handler in self.handlers:
            supported = supported.union(handler.languages())
        return supported

    def supported_languages_for(self, tafsir):
        supported: set = set()
        for handler in self.handlers:
            for language in handler.languages():
                if handler.is_supported(tafsir, language):
                    supported.add(language)
        return list(supported)

    def get_default_language_for(self, tafsir):
        return self.supported_languages_for(tafsir)[0]

    @staticmethod
    def make_embed(data: TafsirData, url, req):
        num_chars = 0
        e = discord.Embed(title=data.tafsir_name + " | " + data.surah_name + " | " + req,
                          color=35810, description=f"[link]({url})\n\n" + data.ayah_text)
        num_chars += len(e.title) + len(e.description)

        txt = data.tafsir_text
        while len(txt) > 0 and txt.isalpha() and num_chars < 5000:
            ind = txt.rfind(' ', 700, 1000)
            part = txt[:ind]
            txt = txt[ind:]
            e.add_field(name='​', value=part, inline=False)  # that's a zero width space
            num_chars += len(part)
        if num_chars >= 5000:
            e.add_field(name='​', value="(Text too long for discord, see link above for full text)", inline=False)  # that's a zero width space
        e.set_thumbnail(url="https://i.imgur.com/BOJeLJF.png")
        return e

