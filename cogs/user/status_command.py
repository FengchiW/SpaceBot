from ..util import sql
import discord


def get_status(gid):
    data = sql.fetch_leaderboard(gid)
    embed=discord.Embed(title="Bot Status", description="Space Bot vr" % data[2], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Uptime", value="%s" % data[6], inline=True)
    embed.add_field(name="Vials", value="%s" % data[8], inline=True)
    embed.add_field(name="Runes", value="%s" % data[7], inline=True)
    embed.add_field(name="Runs", value="%s" % data[5], inline=False)
    return embed