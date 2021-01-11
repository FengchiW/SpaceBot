import discord


def config_embed(options: dict) -> discord.Embed:
    embed = discord.Embed(title="Available Configuration Options",
                          description="Usage: `;config [option] [value]`",
                          color=0x991e31)
    embed.set_thumbnail(url="https://discordapp.com/assets/eed642a423f5147c48ad395310a3d797.svg")
    for option in options:
        embed.add_field(name=option, value=options[option][0], inline=False)
    return embed