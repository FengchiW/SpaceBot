from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context
from cogs.user import headcount
from util.permissions import is_rl_or_higher
from persistent import sql, server_config, sqlconfig

class RaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#    @commands.command(aliases=['hc'])
#    @is_rl_or_higher()
#    async def headcount(self, ctx):
#        await headcount.start_headcount(ctx, self.bot)

#    @commands.command()
#    @is_rl_or_higher()
#    async def afk(self, ctx):
#        await headcount.start_headcount(ctx, self.bot)

async def on_reaction_add(reaction: Reaction, user: User):
    pass


def setup(client):
    client.add_cog(RaidCommands(client))
