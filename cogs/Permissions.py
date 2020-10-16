from discord.ext import commands

class Permissions(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def hasperms(self, ctx):
        return any(
            role in ["Admins", "Owner", "Moderators", "Leader", "Head Leader", "Security"]
            for role in ctx.author.roles)