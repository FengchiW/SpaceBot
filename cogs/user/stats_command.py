import discord
from ..util import sql

def get_stats(gid, uid):
    data = sql.fetch_user(gid, uid)
    embed=discord.Embed(title="Stats", description="Stats for %s" % data['IGN'], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Keys", value="%s" % data['KEYS'], inline=True)
    embed.add_field(name="Vials", value="%s" % data['VIALS'], inline=True)
    embed.add_field(name="Runes", value="%s" % data['RUNES'], inline=True)
    embed.add_field(name="Runs", value="%s" % data['RUNS'], inline=False)
    embed.add_field(name="Points", value="%s" % data['POINTS'], inline=False)
    return embed