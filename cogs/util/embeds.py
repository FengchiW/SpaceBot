import discord
import asyncio

portals = {
    "Shatters": "<:ShattersPortal:524596214847635456>",
    "Parasite": "<:Parasite:761334825919447070>"

}
keys = {
    "Shatters": "<:ShattersKey:524596214843441172>",
    "Parasite": "<:Parasitekey:761334703834791948>"
}
status = {
    "Daze": "<:Daze:761336073765912626>",
    "Warr": "<:Warrior:761335945219538945>",
    "Slow": "<:Slow:761659703004102697>",
    "MSeal": "<:MSeal:761659656853782578>",
    "Mystic": "<:Mystic:524596214805561352>"
}

MIN_TIMED_UPDATE_INTERVAL = 5
DEFAULT_TIMED_UPDATE_INTERVAL = 5


def time_str(time) -> str:
    time_min = time // 60
    time_sec = time % 60
    return "Time remaining: " + str(time_min) + "m " + str(time_sec) + "s"


async def timed_embed(msg, embed, time_remaining, expired_embed, update_interval=DEFAULT_TIMED_UPDATE_INTERVAL) -> None:
    embed.set_footer(text=time_str(time_remaining),
                     icon_url="https://discordapp.com/assets/1b49a181ff7cdab94bd390b3d3224f63.svg")
    await msg.edit(embed=embed)
    # don't update any faster than every 5 seconds by default
    if update_interval < MIN_TIMED_UPDATE_INTERVAL:
        update_interval = MIN_TIMED_UPDATE_INTERVAL
    while True:
        await asyncio.sleep(5)
        time_remaining -= update_interval
        if time_remaining <= 0:
            await msg.edit(embed=expired_embed)
            return
        else:
            embed.set_footer(text=time_str(time_remaining))
            await msg.edit(embed=embed)

def afk_embed(dungeon, user, thumbnail_url="") -> discord.Embed:
    dungeon = str(dungeon).title()
    embed = discord.Embed(title="Raid started: " + dungeon,
                          description="A run  " + dungeon + " has been started by " + user.name + ".",
                          color=0x991e31)
    if thumbnail_url != "":
        embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Please react with the portal icon and any class/gear choices below.",
                    value="React with a key if you're willing to pop it.", inline=True)
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


def verification_embed(guild, rank_req, code) -> discord.Embed:
    embed = discord.Embed(title="How to Verify", url="https://youtu.be/180hrQFK0-c",
                          description="Welcome to " + guild.name + "! Please follow these simple steps below to become "
                                                                   "verified, or click the link above for video "
                                                                   "instructions.",
                          color=0x0062ff)
    embed.set_author(name=guild.name)
    embed.add_field(name="Step 1:", value="Make sure you have at least " + str(rank_req) +
                                          " stars and set your location to hidden on Realmeye.", inline=False)
    embed.add_field(name="Step 2:", value="Your unique code is **" + code + "**. Paste this code into any line of "
                                                                            "your Realmeye description.",
                    inline=False)
    embed.add_field(name="Step 3:", value="Send !confirm [IGN] via DM to <@!761017369560350720>, replacing [IGN] with "
                                          "your in-game name.     Example: !confirm YamaBad", inline=False)
    embed.add_field(name="Step 4:", value="If you followed all the steps correctly you should be verified. If not "
                                          "please ping for help in the Help and Support channel!", inline=False)
    return embed


def verification_expired_embed(guild) -> discord.Embed:
    embed = discord.Embed(title="Verification expired!",
                          description="Your verification for " + guild.name + " has expired.")
    embed.set_author(name=guild.name)
    embed.add_field(name="You may attempt verification again at any time.",
                    value="Simply type ;verify into the appropriate channel once more to restart the process.")
    return embed
