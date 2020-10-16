import discord
from discord.ext import commands
from .util import Permissions
from .user import status_command, leaderboard_command, stats_command


class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="stats", description = "Returns the user's run stats")
    @commands.guild_only()
    async def stats(self, ctx, *args):
        uid = ctx.author.id
        ctx.send(stats_command.get_stats(uid))

    @commands.command(usage="leaderboard", description = "Returns the key poping leaderboard")
    @commands.guild_only()
    async def leaderboard(self, ctx, *args):
        ctx.send(leaderboard_command.leaderboard())

    @commands.command(usage="get_status", description = "Returns current bot stats")
    @commands.guild_only()
    @Permissions.is_Leader_or_higher()
    async def get_status(self, ctx):
        ctx.send(status_command.get_status())

def setup(client):
    client.add_cog(UserCommands(client))

