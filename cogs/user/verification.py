import asyncio
import random
from ..util import sql, constants
from ..util.embeds import verification_embed
import codecs, requests, json

# verify (ign, code) Verifies the user ouputing a code based on a player's realmeye statistics

# Timeout for verification is 900 seconds (15 minutes) by default.
VERIFICATION_TIMEOUT = 900
VERIFY_MSG_DELETE_TIME = 10
MIN_CODE = 100
MAX_CODE = 999

# Temporary cache for verification requests.
verifications = dict()


async def start_verify(ctx):
    uid = ctx.author.id
    sql_data = sql.fetch_user(ctx.guild.id, uid)
    if (sql_data is not None and bool(sql_data[constants.SQL_VERIFIED])) or uid in verifications:
        await ctx.send(":x: **<@" + str(uid) + ">, you're already verified or verifying!**",
                       delete_after=VERIFY_MSG_DELETE_TIME)
        return
    # generate a prefix from the first letters of the guild name, assuming
    # the guild name contains alphabetical characters
    prefix = "".join([s[0] for s in ctx.guild.name.split()])
    # in the event the guild is named something stupid like 35126135623451341, just prefix with ST for Space Travel
    # haha i am funny..
    if prefix == "":
        prefix = "ST"
    # code is just "prefix_randint", ex. "STD_913"
    code = prefix + "_" + str(random.randint(MIN_CODE, MAX_CODE))
    # user with ID uid is verifying for guild with ID gid.
    verifications[uid] = (ctx.guild, code)
    await ctx.send(":rocket: **<@" + str(uid) + ">, message sent!**", delete_after=VERIFY_MSG_DELETE_TIME)
    verify_msg = await ctx.author.send(embed=verification_embed(ctx.guild, 19, code))
    # schedule user to be removed from the verification cache after aset period
    await asyncio.sleep(VERIFICATION_TIMEOUT)
    if uid in verifications:
        verifications.pop(uid)
        await ctx.author.send(":rocket: **Your verification attempt for " + ctx.guild.name + " has expired!**")


def confirm(uid, ign):
    player_data = requests.get(
        'https://nightfirec.at/realmeye-api/?player=' + str(ign) + "&filter=desc1+desc2+desc3+player_last_seen+rank",
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'})

    d = codecs.decode(player_data.content)

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

    if line1.find(code) != -1 or line2.find(code) != -1 or line3.find(code) != -1:
        if rank > 19:
            if location == "hidden":
                # here's where you'd need to actually store their verification status in the server's SQL db
                if sql.fetch_user(guild.id, uid) is not None:
                    sql.update_user(uid, constants.SQL_VERIFIED, "True", guild.id)
                else:
                    sql.add_user(ign, guild.id, uid)
                del verifications[uid]
                return "Successfully verified!"
            else:
                return "Your location is public! Set it to hidden and try again."
        else:
            return "A minimum of 20 stars required you have %s" % (rank)
    else:
        return "Your unique code was not found in your Realmeye description! Your description is:\n%s\n%s\n%s\n\nIf " \
               "you have recently attempted to verify, please wait a few minutes before trying again." % (line1,
                                                                                                          line2, line3)
