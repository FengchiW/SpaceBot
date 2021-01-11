import discord
import asyncio

# Afk embeds
def afk_embed(dungeon, user, thumbnail_url="") -> discord.Embed:
    dungeon = str(dungeon).title()
    embed = discord.Embed(title="Raid started: " + dungeon,
                          description="A raid on " + dungeon + " has been started by " + user.name + ".",
                          color=0x991e31)
    if thumbnail_url != "":
        embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Please react with the portal icon and any class/gear choices below.",
                    value="React with a key if you're willing to pop it.", inline=True)
    return embed

def afk_setup_embed(dungeon, user, thumbnail_url="") -> discord.Embed:
    dungeon = str(dungeon).title()
    embed = discord.Embed(title="Raid started: " + dungeon,
                          description="A raid on " + dungeon + " has been started by " + user.name + ".",
                          color=0x991e31)
    if thumbnail_url != "":
        embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Please react with the portal icon and any class/gear choices below.",
                    value="React with a key if you're willing to pop it.", inline=True)
    return embed

def afk_expired_embed(dungeon, user, thumbnail_url="") -> discord.Embed:
    dungeon = str(dungeon).title()
    embed = discord.Embed(title="Raid started: " + dungeon,
                          description="A raid on " + dungeon + " has been started by " + user.name + ".",
                          color=0x991e31)
    if thumbnail_url != "":
        embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Please react with the portal icon and any class/gear choices below.",
                    value="React with a key if you're willing to pop it.", inline=True)
    return embed