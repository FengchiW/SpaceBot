import discord
from ..util import sql
from ..util import constants

def get_stats(gid, uid):
    data = sql.fetch_user(gid, uid)
    embed = discord.Embed(title="Stats", description="Stats for %s" % data[constants.SQL_IGN], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Keys", value="%s" % data[constants.SQL_KEY_POPS], inline=True)
    embed.add_field(name="Vials", value="%s" % data[constants.SQL_VIALS], inline=True)
    embed.add_field(name="Runes", value="%s" % data[constants.SQL_RUNES], inline=True)
    embed.add_field(name="Runs", value="%s" % data[constants.SQL_RUNS], inline=False)
    embed.add_field(name="Points", value="%s" % data[constants.SQL_POINTS], inline=False)
    return embed
