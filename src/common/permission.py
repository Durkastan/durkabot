from discord.ext.commands import check, MissingPermissions


def has_permissions(**perms):
    def predicate(ctx):
        if ctx.guild is None:
            return False

        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)

        if permissions.administrator or ctx.guild.owner == ctx.author:
            return True

        missing = [perm for perm, value in perms.items() if getattr(permissions, perm, None) != value]

        if not missing:
            return True

        raise MissingPermissions(missing)

    return check(predicate)
