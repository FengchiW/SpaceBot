import asyncio

from discord import Message

MIN_TIMED_UPDATE_INTERVAL = 5
DEFAULT_TIMED_UPDATE_INTERVAL = 5


def time_str(time: int) -> str:
    time_min = time // 60
    time_sec = time % 60
    return "Time remaining: " + str(time_min) + "m " + str(time_sec) + "s"


async def delay_delete(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()


async def timed_embed(msg, embed, time_remaining, expired_embed, update_interval=DEFAULT_TIMED_UPDATE_INTERVAL,
                      condition_predicate=None, completed_embed=None) -> None:
    # set the embed footer to the remaining time
    embed.set_footer(text=time_str(time_remaining))
    # edit the message with remaining time
    await msg.edit(embed=embed)
    # don't update any faster than every 5 seconds by default
    if update_interval < MIN_TIMED_UPDATE_INTERVAL:
        update_interval = MIN_TIMED_UPDATE_INTERVAL
    while True:
        # wait however many seconds
        await asyncio.sleep(update_interval)
        # if the predicate function isn't none
        if condition_predicate is not None:
            try:
                # did it complete this time around?
                completed = condition_predicate()
                # if the predicate function actually returned a bool
                if isinstance(completed, bool):
                    # only do shit if it returns True
                    if completed:
                        # use the completed embed if there is one
                        if completed_embed is not None:
                            await msg.edit(embed=completed_embed)
                        # otherwise it's just expired, f for embed
                        else:
                            await msg.edit(embed=expired_embed)
                        return
            except Exception as e:
                # Don't call again
                condition_predicate = None
                print(e)

        time_remaining -= update_interval
        if time_remaining <= 0:
            await msg.edit(embed=expired_embed)
            return
        else:
            embed.set_footer(text=time_str(time_remaining))
            await msg.edit(embed=embed)