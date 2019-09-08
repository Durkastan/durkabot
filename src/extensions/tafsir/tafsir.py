import discord
from discord.ext import commands

from extensions.tafsir.tafsir_fetcher import TafsirFetcher


class Tafsir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetcher = TafsirFetcher(bot.loop)

    @commands.command()
    async def tafsir(self, ctx, req, tafsir, language='en'):
        embed = self.make_embed(await self.fetcher.fetch(req, tafsir, language))
        await ctx.send(embed=embed)

    @staticmethod
    def make_embed(response):
        e = discord.Embed(title=response.surah_english_name + " | " + response.surah_arabic_name, color=35810)
        for ayah_num, ayah_txt in response.ayahs.items():
            if len(ayah_txt) < 1000:
                e.add_field(name=str(ayah_num), value=ayah_txt, inline=False)
            else:
                ind = ayah_txt.rfind(' ', 700, 1000)
                part_1 = ayah_txt[:ind]
                part_2 = ayah_txt[ind:]
                e.add_field(name=str(ayah_num), value=part_1, inline=False)
                e.add_field(name='​', value=part_2, inline=False)  # that's a zero width space
        e.set_footer(text=f"{response.surah_revelation_type} | {response.edition_name}")
        e.set_thumbnail(url="https://i.imgur.com/BOJeLJF.png")
        return e
