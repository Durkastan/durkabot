import discord
from discord.ext import commands
from discord.ext.commands import Cog

from extensions.hadith.hadithfetcher import HadithFetcher
from extensions.hadith.hadithresponse import HadithResponse

hadith_book_list = ['bukhari', 'muslim', 'tirmidhi', 'abudawud', 'nasai', 'ibnmajah', 'malik', 'riyadussaliheen',
                    'adab', 'bulugh', 'qudsi', 'nawawi']


class Hadith(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetcher = HadithFetcher(bot.loop)

    @commands.command()
    async def hadith(self, ctx, book_name, ref, language='en'):
        if book_name not in hadith_book_list:
            readable_book_list = str(hadith_book_list).strip("[]").replace("'", '')
            await ctx.send(f'Invalid hadith book! These are currently supported: \n`{readable_book_list}`')
            return

        response, link = await self.fetcher.fetch(book_name, ref)
        embed = self.make_embed(response, link, language, ref)
        await ctx.send(embed=embed)

    @staticmethod
    def make_embed(response: HadithResponse, link, language, ref):
        e = discord.Embed(title=response.narrator if language == 'en' else '​', color=35810)  # zero width space
        hadith_text = response.english_text if language == 'en' else response.arabic_text

        e.set_author(name=f"{response.book_title} {ref}", url=link)

        while hadith_text != '':
            if len(hadith_text) < 1000:
                segment = hadith_text
                hadith_text = ''
            else:
                ind = hadith_text.rfind(" ", 0, 1000)
                segment = hadith_text[:ind]
                hadith_text = hadith_text[ind:]

            e.add_field(name='​', value=segment, inline=False)  # zero width space

        footer = f"{response.book_section_name}"
        if response.grading != '':
            footer += " | " + response.grading

        e.set_footer(text=footer)
        e.set_thumbnail(url="https://i.imgur.com/BOJeLJF.png")
        return e
