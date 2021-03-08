from discord import Reaction, User, Embed
from discord.ext import commands
from discord.ext.commands import Context
from cogs.user import headcount
from util.permissions import is_rl_or_higher, is_staff
from persistent import sql, server_config, sqlconfig
from cogs.moderation import parse
from cogs.raid import afkcheck
from discord.utils import get
import re

class RaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["p"])
    @commands.guild_only()
    @is_rl_or_higher()
    async def parse(self, ctx: Context, *args):
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

    @commands.command()
    @commands.guild_only()
    @is_rl_or_higher()
    async def afk(self, ctx: Context, dung = None, location = None, *args):
        peram = args

    @commands.command()
    @commands.guild_only()
    @is_rl_or_higher()
    async def hc(self, ctx: Context, dung = None, location = None, *args):
        peram = args

    @commands.command(aliases=["e", "log", "l"])
    @commands.guild_only()
    @is_staff()
    async def logrun(self, ctx: Context, usr=None):
        pass


def setup(client):
    client.add_cog(RaidCommands(client))
