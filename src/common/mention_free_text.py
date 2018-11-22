from discord.ext.commands import UserInputError


class NotMentionFreeException(UserInputError):
    pass


class MentionFreeText:
    @classmethod
    async def convert(cls, ctx, argument):
        msg = ctx.message

        if (msg.content.find('@everyone') != -1
                or msg.content.find('@here') != -1
                or msg.mentions
                or msg.role_mentions):
            raise NotMentionFreeException("This argument can't contain any mentions!")

        return argument

