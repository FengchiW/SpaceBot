import discord
from discord.ext import commands
from Permissions import Permissions
from user import status_command, leaderboard_command, stats_command


class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, *args):
        uid = ctx.author.id
        ctx.send(stats_command.get_stats(uid))

    @commands.command()
    async def leaderboard(self, ctx, *args):
        ctx.send(leaderboard_command.leaderboard())

    @commands.command()
    @commands.check(Permissions.hasperms)
    async def get_status(self, ctx):
        ctx.send(status_command.get_status())

def setup(client):
    client.add_cog(UserCommands(client))

