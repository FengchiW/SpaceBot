import re

from discord import Guild, Member
from discord.ext.commands import Context
from discord.utils import get

from persistent import server_config, sql
from cogs.moderation import weekly

from util import constants

async def rs(ctx: Context, args):
    if len(args) < 1 or len(args) > 2:
        await ctx.send(":x: **Usage: ;rs [level] [user ID or mention if yourself nothing here]**", delete_after=1000)
        return
    try:
        # prune extraneous symbols from mentions
        level = int(args[0])
        uid = None
        if len(args) == 2:
            uid = int(re.sub('[<!@>]', '', args[1]))
        else:
            uid = ctx.message.author.id

        guild: Guild = ctx.guild
        member: Member = await guild.fetch_member(uid)

        if member is None:
            await ctx.send(":x: **Can't find this member.**", delete_after=500)
            return

        if not await sql.fetch_staff(uid) is None:
            pass
        else:
            await sql.addstaff(uid, level)

        await ctx.message.add_reaction(constants.EMOJI_CONFIRM)
    except ValueError as e:
        await ctx.send(":x: **Argument must be a user's ID or an @mention.** %s " % (e), delete_after=500)
        return
