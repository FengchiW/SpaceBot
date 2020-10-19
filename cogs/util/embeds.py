import discord

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


def afkembed():
    embed = discord.Embed(title="Parasite AFK Check!",
                          description="A Parasite AFK Check has been started by (Insert Rl Name). Join Raiding 1 and react with (Parasite portal) to join!",
                          color=0x991e31)
    embed.set_thumbnail(url="https://i.imgur.com/O43mDnf.gif")
    embed.add_field(name="Bringing Warrior? React with:", value="(helm)", inline=True)
    embed.add_field(name="Bringing Paladin? React with:", value="(tiered Seal)", inline=True)
    embed.add_field(name="Bringing Wizard? React with:", value="(Wizard)", inline=True)
    embed.add_field(name="Bringing Puri? React with:", value="(puri)", inline=True)
    embed.add_field(name="Bringing Daze? React with:", value="(Qot)", inline=True)
    embed.add_field(name="Booster? React with:", value="(Booster Logo) To get early location", inline=True)
    return embed


def verification_embed(guild, rank_req, code):
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
