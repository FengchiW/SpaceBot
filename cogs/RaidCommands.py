
import discord
from discord.ext import commands
import sql
import time


class RaidCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def hasperms(self, ctx):
        return  any(
            role in ["Admins", "Owner", "Moderators", "Leader", "Head Leader", "Security"]
            for role in ctx.author.roles)
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
    
    @commands.command()
    async def stats(self, ctx, *args):
        uid = 235241036388106241
        if len(args) == 0:
            uid = int(ctx.author.id)
            data = sql.fetch_user(uid)
            embed=discord.Embed(title="Stats", description="Stats for %s" % data[2], color=0xffffff)
            embed.set_author(name="Space Bot")
            embed.add_field(name="Keys", value="%s" % data[6], inline=True)
            embed.add_field(name="Vials", value="%s" % data[8], inline=True)
            embed.add_field(name="Runes", value="%s" % data[8], inline=True)
            embed.add_field(name="Runs", value="%s" % data[5], inline=False)
            ctx.send(embed=embed)
    
    @commands.command()
    @commands.check(hasperms)
    async def get_status(self, ctx):
        embed=discord.Embed(title="Bot Status", description="Space Bot vr 1.02", color=0xffffff)
        embed.set_author(name="Space Bot")
        embed.add_field(name="Uptime", value="Null", inline=True)
        ctx.send(embed = embed)

def setup(client):
    client.add_cog(RaidCommands(client))

starttime = time.time()

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

def get_stats(uid):
    data = sql.fetch_user(uid)
    embed=discord.Embed(title="Stats", description="Stats for %s" % data[2], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Keys", value="%s" % data[6], inline=True)
    embed.add_field(name="Vials", value="%s" % data[8], inline=True)
    embed.add_field(name="Runes", value="%s" % data[8], inline=True)
    embed.add_field(name="Runs", value="%s" % data[5], inline=False)
    return embed

def get_status(uid):
    embed=discord.Embed(title="Bot Status", description="Space Bot vr" % data[2], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Uptime", value="%s" % data[6], inline=True)
    embed.add_field(name="Vials", value="%s" % data[8], inline=True)
    embed.add_field(name="Runes", value="%s" % data[8], inline=True)
    embed.add_field(name="Runs", value="%s" % data[5], inline=False)
    return embed