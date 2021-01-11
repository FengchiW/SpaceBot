import discord
import asyncio

#HeadCountEmbeds
def headcount_setup_embed() -> discord.Embed:
    embed = discord.Embed(title="Setting up a headcount.",
                          description="Select the reaction for the corresponding dungeon below, then react with "
                                      ":white_check_mark: to start the headcount.",
                          color=0x991e31)
    embed.add_field(name="Mistake? Suddenly not feeling it?", value="React with the :x: to cancel.")
    return embed


def headcount_embed(dungeon, user, thumbnail_url="") -> discord.Embed:
    dungeon = str(dungeon).title()
    embed = discord.Embed(title="Headcount for " + dungeon,
                          description="A headcount for " + dungeon + " has been started by " + user.name + ".",
                          color=0x991e31)
    if thumbnail_url != "":
        embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Please react with the portal icon and any class/gear choices below.",
                    value="React with a key if you're willing to pop it.", inline=True)
    return embed


def headcount_expired_embed():
    embed = discord.Embed(title="This headcount has ended.", description="Please wait for an RL to start another.",
                          color=0x991e31)
    return embed