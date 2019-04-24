from extensions.hadith.hadith import Hadith


def setup(bot):
    bot.add_cog(Hadith(bot))
