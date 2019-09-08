from extensions.tafsir.tafsir import Tafsir


def setup(bot):
    bot.add_cog(Tafsir(bot))
