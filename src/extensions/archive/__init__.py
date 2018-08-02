from extensions.archive.archive import Archive


def setup(bot):
    bot.add_cog(Archive(bot))
