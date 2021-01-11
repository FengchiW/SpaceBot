import discord


def stats_embed(guild, user, rank_req, code) -> discord.Embed:
    embed = discord.Embed(title="How to Verify", url="https://youtu.be/180hrQFK0-c",
                          description="Welcome to " + guild.name + "! Please follow these simple steps below to become "
                                                                   "verified, or click the link above for video "
                                                                   "instructions.",
                          color=0x0062ff)
    embed.set_author(name=user.displayname)
    embed.add_field(name="Step 1:", value="Make sure you have at least " + str(rank_req) +
                                          " stars and set your location to hidden on Realmeye.", inline=False)
    embed.add_field(name="Step 2:", value="Your unique code is **" + code + "**. Paste this code into any line of "
                                                                            "your Realmeye description.",
                    inline=False)
    embed.add_field(name="Step 3:", value="Send ;confirm [IGN] in this DM channel, replacing [IGN] with "
                                          "your in-game name.     Example: !confirm MassiveEgg", inline=False)
    embed.add_field(name="Step 4:", value="If you followed all the steps correctly you should be verified. If not "
                                          "please ping for help in the Help and Support channel!", inline=False)
    return embed
