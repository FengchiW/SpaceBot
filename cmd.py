import sql
import discord


def get_stats(uid):
    data = sql.fetch_user(uid)
    embed=discord.Embed(title="Stats", description="Stats for %s" % data[2], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Keys", value="%s" % data[6], inline=True)
    embed.add_field(name="Vials", value="%s" % data[8], inline=True)
    embed.add_field(name="Runes", value="%s" % data[7], inline=True)
    embed.add_field(name="Runs", value="%s" % data[5], inline=False)
    return embed

def get_leaderboard():
    data = sql.fetch_leaderboard()
    embed=discord.Embed(title="LeaderBoard", description="Top 10 Key Poppers", color=0xffffff)
    embed.set_author(name="Space Bot")
    for i in range(len(data)):
        embed.add_field(name="#%s" % (i+1), value="%s : %s Keys" % (data[i][2], data[i][6]), inline=False)
    return embed

def get_status():
    data = sql.fetch_leaderboard()
    embed=discord.Embed(title="Bot Status", description="Space Bot vr" % data[2], color=0xffffff)
    embed.set_author(name="Space Bot")
    embed.add_field(name="Uptime", value="%s" % data[6], inline=True)
    embed.add_field(name="Vials", value="%s" % data[8], inline=True)
    embed.add_field(name="Runes", value="%s" % data[7], inline=True)
    embed.add_field(name="Runs", value="%s" % data[5], inline=False)
    return embed