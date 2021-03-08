import asyncio

from discord.ext.commands import Context

from util.embeds.headcount_embeds import headcount_embed, headcount_expired_embed, headcount_setup_embed

from util.message_util import timed_embed

HEADCOUNT_TIMEOUT = 900
HEADCOUNT_MSG_DELETE_TIME = 10

# cache for ongoing headcounts
headcounts = dict()


async def start_headcount(ctx: Context, bot):
    # user with ID uid is verifying for guild with ID gid.
    uid = ctx.author.id
    if uid in headcounts:
        await ctx.send(":x: **<@" + str(
            uid) + ">, you've already started a headcount! Either end it or wait before starting a new one.**",
                       delete_after=HEADCOUNT_MSG_DELETE_TIME)
        return

    embed = headcount_setup_embed()
    headcount_setup_msg = await ctx.send(embed=embed)

    headcounts[uid] = []

    asyncio.create_task(timed_embed(headcount_setup_msg, embed, HEADCOUNT_TIMEOUT, headcount_expired_embed(),
                                    condition_predicate=lambda: uid not in headcounts,
                                    completed_embed=headcount_expired_embed()))
    # schedule user to be removed from the verification cache after a set period
    await headcount_setup_msg.add_reaction("❌")
    await headcount_setup_msg.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '✅'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        headcounts[uid].append(reaction)
    except asyncio.TimeoutError:
        await headcount_setup_msg.edit(embed=headcount_expired_embed())
        if uid in headcounts:
            headcounts.pop(uid)
        await headcount_setup_msg.clear_reactions()
    else:
        await headcount_setup_msg.edit(embed=headcount_embed("Test", ctx.author))
        if uid in headcounts:
            headcounts.pop(uid)
        await headcount_setup_msg.clear_reactions()

