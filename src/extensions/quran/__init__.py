from extensions.quran.quran import Quran


def setup(bot):
    bot.add_cog(Quran(bot))
