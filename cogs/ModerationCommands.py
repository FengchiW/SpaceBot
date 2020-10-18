import discord
from discord.ext import commands
from .util import Permissions
from .user import get_status, manver, connectdb


class ModerationCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        connectdb()

    @commands.command(aliases = ["mv", "adduser", "au"], usage="@<User> IGN", description = "Returns the user's run stats", case_insensitive = True)
    @commands.guild_only()
    async def manver(self, ctx, user, ign):
        uid = int(user[3:-1])
        manver(ign, uid, ctx.guild.id)
        await ctx.send("verified")
    
    @commands.command(description = "Connects the database", case_insensitive = True)
    @commands.guild_only()
    async def connectdb(self, ctx):
        await ctx.send("%s" % (connectdb()))
    
    @commands.command(usage="purge", description = "Purges and Archives the current channel", case_insensitive = True)
    @commands.guild_only()
    @commands.check(Permissions.is_Leader_or_higher)
    async def purge(self, ctx, arg):
        await ctx.message.channel.purge(limit = int(arg))

def setup(client):
    client.add_cog(ModerationCommands(client))

