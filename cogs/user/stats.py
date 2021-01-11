from discord.ext.commands import Context
from emojis import encode
from util import constants

from discord import Embed

from persistent import sql

#INCOMPLETE
async def getstats(ctx: Context, args = None):
    gid = ctx.guild.id
    uid = ctx.author.id

    user = await sql.fetch_user(gid, uid)

    print(user)

    embed=Embed(title="Stats", description="%s"%(ctx.author.display_name))
    embed.add_field(name="Keys", value="%s" % (user[constants.SQL_KEY_POPS]), inline=True)
    embed.add_field(name="Vials", value="%s" % (user[constants.SQL_VIALS]), inline=True)
    embed.add_field(name="Runes", value="%s" % (user[constants.SQL_RUNES]), inline=True)
    embed.add_field(name="O3", value="%s" % (user[constants.SQL_O3]), inline=True)
    embed.add_field(name="Runs", value="%s" % (user[constants.SQL_RUNS]), inline=True)
    embed.add_field(name="Points", value="%s" % (user[constants.SQL_POINTS]), inline=True)

    await ctx.send(embed=embed)