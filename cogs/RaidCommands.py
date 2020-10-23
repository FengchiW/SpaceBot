import discord
from discord.ext import commands
from .raid import headcount_command
from .util import sql
import time

DEFAULT_HEADCOUNT_TIME = 300


def get_raiding_channel(server):
    for channel in server.channels:
        if channel.name == "│raid-status":
            return channel


class RaidCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="afk", aliases=["raid"], case_insensitive=True)
    @commands.guild_only()
    async def afk(self, ctx, *args):
        # todo: start afk check
        pass

    @commands.command(usage="headcount", description="Starts a headcount.")
    @commands.guild_only()
    async def headcount(self, ctx, *args):
        if len(args) > 0:
            dungeon_name = str(args[0])
            headcount_time = DEFAULT_HEADCOUNT_TIME
            if len(args) > 1:
                headcount_time = int(args[1])
                # todo: give the RL a headcount setup embed instead of just starting one
            await headcount_command.start_headcount(ctx, dungeon_name, headcount_time)
        else:
            await ctx.send("**Usage:**```headcount [dungeon name] <headcount duration in seconds>```")


def setup(client):
    client.add_cog(RaidCommands(client))
