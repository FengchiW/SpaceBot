from ..util import sql
import discord

def leaderboard(gid):
    data = sql.fetch_leaderboard(gid)
    embed = discord.Embed(title="LeaderBoard", description="Top 10 Key Poppers", color=0xffffff)
    embed.set_author(name="Space Bot")
    for i in range(len(data)):
        embed.add_field(name="#%s" % (i + 1), value="%s : %s Keys" % (data[i][2], data[i][6]), inline=False)
    return embed