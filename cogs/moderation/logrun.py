import re
from discord import Embed
from util import constants

async def log_run(ctx, usr, bot):
    if not usr is None:
        uid = re.sub('[<!@>]', '', usr)
        if int(uid) < 10:
            p = int(uid)
            uid = ctx.author.id
    else:
        uid = ctx.author.id
    
    def check(obj, user = 0):
        if user == 0:
            return obj.author.id == uid
        else:
            return obj.message == msg and user.id != bot.user.id

    # await ctx.send("```Error invalid usage,\n `Usage: .l <runs> <type (see below)> <uid/mention (*optional yourself if none)> <pots (*optional default=3)>` \n  `Types: (halls, o3, exalt, misc, failed)````")
    embed = Embed(title="Run Logging Assistant", description="=========================")
    
    embed.add_field(name = "What kind of run do you want to log.", value="1️⃣: O3\n 2️⃣: Halls\n 3️⃣: Exalt\n 4️⃣: Other\n ❌: Cancel\n", inline=False)
    msg = await ctx.send(embed=embed)

    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")
    await msg.add_reaction("❌")

    contract = await bot.wait_for('reaction_add', check=check)
    run_type = 0
    num = 0
    pots = 3
    t_continue = True

    if contract[0].emoji == "1️⃣":
        run_type = 1
    elif contract[0].emoji == "2️⃣":
        run_type = 0
    elif contract[0].emoji == "3️⃣":
        run_type = 2
    elif contract[0].emoji == "4️⃣":
        run_type = 3
    elif contract[0].emoji == "❌":
        await msg.edit(content = "Bye!")
        t_continue = False

    await msg.clear_reactions()
    
    if t_continue:
        embed = Embed(title="Run Logging Assistant", description="=========================")
        embed.add_field(name = "How many runs?", value="Enter/Type a number below:", inline=False)

        await msg.edit(embed=embed)
        contract = await bot.wait_for('message', check=check)

        num = int(contract.content)
        if num > 100:
            num = 0
        await contract.delete()

        if run_type == 0:
            embed = Embed(title="Run Logging Assistant", description="=========================")
            embed.add_field(name = "Was it a cult?", value="✔: Yes, ❌: no", inline=False)
            await msg.edit(embed=embed)
            await msg.add_reaction("✔")
            await msg.add_reaction("❌")
            contract = await bot.wait_for('reaction_add', check=check)
            if contract[0].emoji == "✔":
                pots = 0
            else:
                pass

            await msg.clear_reactions()

            if pots != 0:
                embed = Embed(title="Run Logging Assistant", description="=========================")
                embed.add_field(name = "How many pots?", value="Enter/Type a number below (average for the runs 0-6):", inline=False)
                await msg.edit(embed=embed)
                contract = await bot.wait_for('message', check=check)
                pots = int(contract.content)
                await contract.delete()

    await sql.log_run(uid, run_type, num, pots)
    await msg.delete()
    
    await ctx.message.add_reaction(constants.EMOJI_CONFIRM)

    logchannel = get(ctx.guild.channels, id=761788719685435404)
    rt = ""
    if run_type == 0:
        rt = "Halls"
    elif run_type == 1:
        rt = "O3's"
    elif run_type == 2:
        rt = "Exalted"
    elif run_type == 3:
        rt = "Misc"
    else:
        rt = "Unknown"
    embed=Embed(title="Runs Logged", description="<@!%s> logged %s %s runs" % (uid, num, run_type))
    await logchannel.send(embed=embed)