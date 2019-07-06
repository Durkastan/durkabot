from extensions.config.config import Config


def setup(bot):
    bot.add_cog(Config(bot))