from discord.ext import commands

def is_Leader_or_higher():
    """Check if user has security or higher roles"""
    def predicate(ctx):
         return any(
            role in ["Admins", "Owner", "Moderators", "Leader", "Head Leader", "Security"]
            for role in ctx.author.roles)
    return commands.check(predicate)