
import discord
from discord.ext import commands
from .util import sql
import time

class RaidCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def getraidingchannel(self, server):
        for channel in server.channels:
            if channel.name == "│raid-status":
                return channel

    @commands.command(usage="headcount", description = "Starts a headcount")
    @commands.guild_only()
    async def Headcount(self, ctx, dungeon = None):
        if not dungeon is None:
            server = ctx.guild
            rc = self.getraidingchannel(server)

            embed=discord.Embed(title="Headcount for %s" % (dungeon))
            embed.set_author(name="Space Ship Bot")
            embed.add_field(name="If you want to participate react with the reactions below", value="react with ✅ to participate", inline=True)

            await rc.send(embed=embed)

        else:
            embed=discord.Embed(title="Headcount Help" % (dungeon))
            embed.set_author(name="Space Ship Bot")
            embed.add_field(name="The Following deongeons are avalible", value="Fungle, Shatts, Halls, Parasyte", inline=True)

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(RaidCommands(client))
