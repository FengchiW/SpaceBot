from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context
from cogs.user import headcount
from util.permissions import is_rl_or_higher
from persistent import sql, server_config, sqlconfig
from cogs.moderation import parse

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
