import discord
from discord.ext import commands
from .util import Permissions
from .user import get_stats, leaderboard, get_status


class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="IGN", description = "confirms the user", case_insensitive = True)
    @commands.dm_only()
    async def confirm(self, ctx, *args):
        uid = ctx.author.id
        await ctx.send(embed = get_stats(ctx.guild.id, uid))

    @commands.command(description = "verify the user", case_insensitive = True)
    @commands.guild_only()
    async def verify(self, ctx, *args):
        uid = ctx.author.id
        await ctx.send(embed = get_stats(ctx.guild.id, uid))

    @commands.command(usage="stats", description = "Returns the user's run stats", case_insensitive = True)
    @commands.guild_only()
    async def stats(self, ctx, *args):
        uid = ctx.author.id
        await ctx.send(embed = get_stats(ctx.guild.id, uid))

    @commands.command(aliases = ["lb"], usage="leaderboard", description = "Returns the key poping leaderboard", case_insensitive = True)
    @commands.guild_only()
    async def leaderboard(self, ctx, *args):
        await ctx.send(embed = leaderboard(ctx.guild.id))

    @commands.command(description = "Returns current bot stats", case_insensitive = True)
    @commands.guild_only()
    @commands.check(Permissions.is_Leader_or_higher)
    async def getstatus(self, ctx):
        await ctx.send(embed = get_status(ctx.guild.id))
    
def setup(client):
    client.add_cog(UserCommands(client))

