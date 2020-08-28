import discord
from discord.ext import commands

from extensions.tafsir.handlers.altafsir import AlTafsir


class Tafsir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.handler = AlTafsir(bot.loop)

    @commands.command()
    async def tafsir(self, ctx, req, tafsir, language='en'):
        embed = self.make_embed(*(await self.handler.fetch(req, tafsir, language)), req)
        await ctx.send(embed=embed)

    @staticmethod
    def make_embed(response, url, req):
        e = discord.Embed(title=response.tafsir_name + " | " + response.surah_name + " | " + req,
                          color=35810, description=f"[link]({url})\n\n" + response.ayah_text)
        txt = response.tafsir_text
        while len(txt) > 0 and not txt.isspace():
            ind = txt.rfind(' ', 700, 1000)
            part = txt[:ind]
            txt = txt[ind:]
            e.add_field(name='​', value=part, inline=False)  # that's a zero width space
        e.set_thumbnail(url="https://i.imgur.com/BOJeLJF.png")
        return e
