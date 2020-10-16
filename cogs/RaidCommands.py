
import discord
from discord.ext import commands
import sql
import time

class RaidCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    def Headcount(message, rc):
        if len(message.content.split(" ")) > 1:
            server = message.guild

            dungeon = message.content.split(" ")[1]

            embed=discord.Embed(title="Headcount for %s" % (dungeon))
            embed.set_author(name="Space Ship Bot")
            embed.add_field(name="If you want to participate react with the reactions below", value="react with ✅ to participate", inline=True)

            rc.send(embed=embed)

            return msg
        else:
            embed=discord.Embed(title="Headcount Help" % (dungeon))
            embed.set_author(name="Space Ship Bot")
            embed.add_field(name="The Following deongeons are avalible", value="Fungle, Shatts, Halls, Parasyte", inline=True)

            rc(server, "│raid-bot-commands").send(embed=embed)

def setup(client):
    client.add_cog(RaidCommands(client))
