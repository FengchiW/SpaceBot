from ..util.embeds import headcount_embed, timed_embed, headcount_expired_embed
import asyncio
from discord.utils import get

active_headcounts = dict()

async def setup_headcount(ctx):
    instance = (ctx.author.id, ctx.guild.id)
    # todo: headcount setup embed here
    pass


async def start_headcount(ctx, dungeon, time):
    embed = headcount_embed(dungeon, ctx.author)
    headcount_msg = await ctx.send(embed=embed)
    asyncio.create_task(timed_embed(headcount_msg, embed, time, headcount_expired_embed()))
    # todo: add the dungeon portal emoji first, then the role reacts (class/gear icons)
    #for emoji in ctx.guild.emojis:
        #await headcount_msg.add_reaction(emoji)
        #await asyncio.sleep(1)

    # when the headcount expires
    await asyncio.sleep(time)
    instance = (ctx.author.id, ctx.guild.id)
    if instance in active_headcounts:
        active_headcounts.pop(instance)
