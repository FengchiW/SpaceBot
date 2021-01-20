import re

from discord import Guild, Member
from discord.ext.commands import Context
from discord.utils import get

from persistent import server_config, sql
from util import constants


async def manual_verify(ctx: Context, args):
    if len(args) < 2:
        await ctx.send(":x: **Usage: ;mv [user ID or mention] [IGN]**")
        return
    try:
        # prune extraneous symbols from mentions
        uid = int(re.sub('[<!@>]', '', args[0]))
        ign = str(args[1])
        guild: Guild = ctx.guild

        mv_channel = get(guild.channels, id=801591104847347762)

        member: Member = await guild.fetch_member(uid)

        def check(m):
            return m.author.id == member.id or member.id == ctx.author.id

        if member is None:
            await ctx.send(":x: **Can't find this member.**", delete_after=500)
            return

        await mv_channel.purge(limit=10, check=check)
        # Fetch the server's config to get the verified role ID.
        cfg = await server_config.get_config(guild)
        member_role = get(cfg.guild.roles, id=cfg.verified_role_id)
        # Put the user in the DB if they're not there already, or just update their verification status.
        if await sql.fetch_user(guild.id, uid) is not None:
            await sql.update_user(uid, constants.SQL_VERIFIED, "True", guild.id)
        else:
            await sql.add_user(guild.id, uid, ign)
        # Then add the verified role and change their nickname.
        # todo: put this common code into a single function in verify.py
        try:
            if member_role is not None:
                await member.add_roles(member_role)
            await member.edit(nick=ign)
        except Exception as e:
            print(e)
        await ctx.message.add_reaction(constants.EMOJI_CONFIRM)
        await mv_channel.purge(limit=10, check=check)
    except ValueError:
        await ctx.send(":x: **Argument must be a user's ID or an @mention.**", delete_after=500)
        return
