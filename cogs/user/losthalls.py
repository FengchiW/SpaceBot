from random import shuffle, randrange
from util.embeds.losthallsgame_embed import halls_embed
import asyncio
 
activegames = {}



async def start_game(ctx, bot):
    # user with ID uid is verifying for guild with ID gid.
    uid = ctx.author.id
    if uid in activegames:
        await ctx.send(":x: **<@" + str(
            uid) + ">, you've already started a Game! Either end it or wait before starting a new one.**",
                       delete_after=10)
        return

    activegames[uid] = {"Name":ctx.author.display_name,
                        "Turn": 0,
                        "Position": (0,0),
                        "Map": await make_maze(9,9)}

    embed = halls_embed(activegames[uid]["Map"], 
                        activegames[uid]["Position"],
                        activegames[uid]["Name"], 
                        activegames[uid]["Turn"])

    losthallsgamemsg = await ctx.send(embed=embed)

    # schedule user to be removed from the verification cache after a set period
    await losthallsgamemsg.add_reaction("⬆")
    await losthallsgamemsg.add_reaction("⬅")
    await losthallsgamemsg.add_reaction("➡")
    await losthallsgamemsg.add_reaction("⬇")
    await losthallsgamemsg.add_reaction("❎")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '❎'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=1000.0, check=check)
    except asyncio.TimeoutError:
        await losthallsgamemsg.edit(content="```Time Out```", embed = None)
        if uid in activegames:
            activegames.pop(uid)
        await losthallsgamemsg.clear_reactions()
    else:
        await losthallsgamemsg.edit(content="```Game Ended```", embed = None)
        if uid in activegames:
            activegames.pop(uid)
        await losthallsgamemsg.clear_reactions()

async def make_maze(w = 16, h = 8):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|󠀠  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
 
    walk(randrange(w), randrange(h))
 
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s

async def draw_map(hmap):
    out = ""
    for r in range(9):
        for c in range(9):
            paths = hmap[r][c][1]
            out += "┌%s┐\n"%(paths[0])
        for c in range(9):
            room = hmap[r][c][0]
            paths = hmap[r][c][1]
            out += "%s%s%s\n"%(paths[2], room, paths[3])
        for c in range(9):
            paths = hmap[r][c][1]
            out += "└%s┘\n"%(paths[1])
        out += "\n"