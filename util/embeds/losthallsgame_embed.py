import discord
import asyncio

def halls_embed(cmap, location, player, turn, thumbnail_url="") -> discord.Embed:
    embed = discord.Embed(title="Lost Halls Map Reading Game",
                          description="Player: %s  | Turn: %s"%(player, turn),
                          color=0x991e31)
    if thumbnail_url != "":
        embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Map",
                    value="```"+cmap+"```", inline=True)
    return embed