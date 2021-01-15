from discord import Reaction, User, Guild
from discord.ext import commands
from discord.ext.commands import Context
from cogs.user import verify, losthalls, stats


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send("Pong!")

    @commands.command(aliases=["Verify", "v", "varify", "VERIFY"])
    @commands.guild_only()
    async def verify(self, ctx: Context):
        await verify.start_verification(ctx)

    @commands.command()
    async def stats(self, ctx: Context):
        #await statsembed = stats.getstats(ctx)
        await stats.getstats(ctx)

    @commands.command()
    async def hpt(self, ctx: Context):
        await losthalls.start_game(ctx, self.bot)
    
    @commands.command(aliases = ['leaderboard'])
    async def lb(self, ctx: Context, *args):
        await stats.lb(ctx, args)

    @commands.command()
    @commands.dm_only()
    async def confirm(self, ctx: Context, *args):
        if len(args) == 0:
            await ctx.send("**Usage: `;confirm [IGN]`**")
        else:
            await ctx.send(await verify.confirm(ctx.author, args[0]))

def setup(client):
    client.add_cog(UserCommands(client))
