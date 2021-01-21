from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context
from cogs.user import headcount
from util.permissions import is_rl_or_higher, is_staff
from persistent import sql, server_config, sqlconfig
from cogs.moderation import parse
import re
from util import constants

class RaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["parse"])
    @commands.guild_only()
    @is_rl_or_higher()
    async def survived(self, ctx: Context, *args):
        attachments = ctx.message.attachments
        if len(attachments) == 0:
            if len(args) == 0:
                await ctx.send(":x: **You must attach a screenshot of /list for this command to work.**")
                return
            else:
                img_url = args[0]
        else:
            img_url = attachments[0].url

        await parse.text_from_image(ctx, img_url)

    @commands.command(aliases=["e", "log", "l"])
    @commands.guild_only()
    @is_staff()
    async def logrun(self, ctx: Context, runs=None, t=None, usr='0', pots=3):
        p = pots
        if runs is None or t is None:
            await ctx.send("```Error invalid usage,\n `Usage: .l <runs> <type (see below)> <uid/mention (*optional yourself if none)> <pots (*optional default=3)>` \n  `Types: (halls, o3, exalt, misc, failed)````")
        uid = re.sub('[<!@>]', '', usr)
        if int(uid) < 10:
            p = int(uid)
            uid = ctx.author.id

        if t.lower() == "halls" or t.lower == 'lh':
            await sql.log_run(uid, 0, runs, pots)
        elif t.lower() == "o3":
            await sql.log_run(uid, 1, runs)
        elif t.lower() == "exalt":
            await sql.log_run(uid, 2, runs)
        elif t.lower() == "misc":
            await sql.log_run(uid, 3, runs)
        elif t.lower() == "failed":
            await sql.log_run(uid, 4, runs)
        
        await ctx.message.add_reaction(constants.EMOJI_CONFIRM)
#    @commands.command(aliases=['hc'])
#    @is_rl_or_higher()
#    async def headcount(self, ctx):
#        await headcount.start_headcount(ctx, self.bot)

#    @commands.command()
#    @is_rl_or_higher()
#    async def afk(self, ctx):
#        await headcount.start_headcount(ctx, self.bot)

async def on_reaction_add(reaction: Reaction, user: User):
    pass


def setup(client):
    client.add_cog(RaidCommands(client))
