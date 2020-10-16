import discord
from ..util import sql

def get_stats(uid):
    data = sql.fetch_user(uid)
    embed=discord.Embed(title="Stats", description="Stats for %s" % data[2], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Keys", value="%s" % data[6], inline=True)
    embed.add_field(name="Vials", value="%s" % data[8], inline=True)
    embed.add_field(name="Runes", value="%s" % data[7], inline=True)
    embed.add_field(name="Runs", value="%s" % data[5], inline=False)
    return embed