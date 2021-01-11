import asyncio
import codecs
import json
import random
from urllib.request import Request, urlopen

import requests
from discord import Member, User
from discord.ext.commands import Context
from discord.utils import get

from util.embeds.verification_embeds import verification_embed, verification_success_embed, verification_expired_embed
from util import constants
from persistent import sql, server_config

# constants, very cool
from util.message_util import timed_embed, delay_delete

VERIFICATION_TIMEOUT = 900
VERIFY_MSG_DELETE_TIME = 10
MIN_CODE = 100
MAX_CODE = 999

# cache for ongoing verifications
verifications = dict()


async def start_verification(ctx: Context, delete_cmd: bool = True):
    global verifications
    uid = ctx.author.id

    # schedule deletion of verify message; might make this configurable later
    if delete_cmd:
        asyncio.create_task(delay_delete(ctx.message, VERIFY_MSG_DELETE_TIME))

    sql_data = await sql.fetch_user(ctx.guild.id, uid)
    if sql_data is not None and bool(sql_data[constants.SQL_VERIFIED]):
        await ctx.send(":x: **<@" + str(uid) + ">, you're already verified!**",
                       delete_after=VERIFY_MSG_DELETE_TIME)
        return
    elif uid in verifications:
        await ctx.send(":x: **<@" + str(uid) + ">, you're already verifying!**",
                       delete_after=VERIFY_MSG_DELETE_TIME)
        return

    # generate a prefix from the first letters of the guild name, assuming
    # the guild name contains alphabetical characters
    prefix = "".join([s[0] if s[0].isalnum() else "" for s in ctx.guild.name.split()])
    # in the event the guild is named something stupid like 35126135623451341, just prefix with ST for Space Travel
    if prefix == "":
        prefix = "ST"
    # code is just "prefix_randint", ex. "STD_913"
    code = prefix + "_" + str(random.randint(MIN_CODE, MAX_CODE))
    # fetch min rank from server config
    min_rank = (await server_config.get_config(ctx.guild)).min_rank
    embed = verification_embed(ctx.guild, min_rank, code)
    # try to send them the verification embed
    verify_msg = await ctx.author.send(embed=embed)

    # Notify them of verification in channel and send DM
    if verify_msg is not None:
        # only cache their current verification attempt if the verification message was actually sent
        verifications[uid] = (ctx.guild, code)
        # timed embed
        asyncio.create_task(timed_embed(verify_msg, embed, VERIFICATION_TIMEOUT, verification_expired_embed(ctx.guild),
                                        condition_predicate=lambda: uid not in verifications,
                                        completed_embed=verification_success_embed(ctx.guild)))
        await ctx.send(":rocket: **<@" + str(uid) + ">, message sent!**", delete_after=VERIFY_MSG_DELETE_TIME)

        # schedule user to be removed from the verification cache after a set period
        await asyncio.sleep(VERIFICATION_TIMEOUT)
        if uid in verifications:
            del verifications[uid]


async def confirm(user: User, ign):
    uid = user.id
    realmeye_url = 'https://nightfirec.at/realmeye-api/?player=' + str(ign) + "&filter=desc1+desc2+desc3+player_last_seen+rank"
    req = Request(realmeye_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                  'Chrome/50.0.2661.102 Safari/537.36'})
    player_data = urlopen(req)
    d = codecs.decode(player_data.read())

    data = json.loads(d)
    line1 = ""
    line2 = ""
    line3 = ""
    rank = -1

    try:
        line1 = data["desc1"]
    except Exception as e:
        print(e)
    try:
        line2 = data["desc2"]
    except Exception as e:
        print(e)
    try:
        line3 = data["desc3"]
    except Exception as e:
        print(e)

    try:
        rank = data["rank"]
    except Exception as e:
        print(e)

    try:
        location = data["player_last_seen"]
    except Exception as e:
        print(e)

    if uid not in verifications:
        return "You are not currently verifying for any server, or your verification has timed out."
    guild = verifications[uid][0]
    code = verifications[uid][1]

    cfg = await server_config.get_config(guild)
    member: Member = await cfg.guild.fetch_member(uid)
    member_role = get(cfg.guild.roles, id=cfg.verified_role_id)
    min_rank = cfg.min_rank

    if line1.find(code) != -1 or line2.find(code) != -1 or line3.find(code) != -1:
        if rank > min_rank:
            if location is not None and location == "hidden":
                # here's where you'd need to actually store their verification status in the server's SQL db
                if await sql.fetch_user(guild.id, uid) is not None:
                    await sql.update_user(uid, constants.SQL_VERIFIED, "True", guild.id)
                else:
                    await sql.add_user(guild.id, uid, ign)
                del verifications[uid]
                try:
                    if member_role is not None:
                        await member.add_roles(member_role)
                    await member.edit(nick=ign)
                except Exception as e:
                    print(e)
                return "Successfully verified!"
            else:
                return "Your location is public! Set it to hidden and try again."
        else:
            return "A minimum of %s stars is required to join this server. You have %s." % (min_rank, rank)
    else:
        return "Your unique code was not found in your Realmeye description! Your description is:```%s\n%s\n%s```If " \
               "you have recently attempted to verify, please wait a few minutes before trying again." % (line1,
                                                                                                          line2, line3)
