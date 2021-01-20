from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context
from persistent import sql, server_config, sqlconfig
from util import constants
from cogs.moderation import config, manual_verify
from util.permissions import is_rl_or_higher
import simplejson as json
from discord import Embed
from discord.utils import get

developers = [218169424132177920, 235241036388106241]


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send("Loaded extension %s." % (extension))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')

        await ctx.send("Unloaded extension %s." % (extension))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')

        await ctx.send("Reloaded extension %s." % (extension))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        await ctx.send("``` Space Bot powering down, good night! ```")
        await self.bot.logout()


    @commands.command()
    async def destroy(self, ctx: Context):
        if ctx.author.id not in developers:
            await ctx.send(":no_entry: **Only developers may perform this action.**")
        else:
            await ctx.send("**Dropping table " + constants.SQL_CONFIG_TABLE_NAME + ".**")
            await sql.drop_table(constants.SQL_CONFIG_TABLE_NAME)
            await ctx.send("**Attempted to drop table " + constants.SQL_CONFIG_TABLE_NAME + "**.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: Context, *args):
        # todo PERMISSIONS
        if len(args) > 0 and str(args[0] == "clear"):
            await ctx.send("**Clearing existing data...**")

        cfg = await sqlconfig.fetch_config(ctx.guild.id)
        if cfg is not None:
            await ctx.send(":x: **This server has already been set up!**")
        else:
            await ctx.send(":rocket: **Performing first-time setup for " + ctx.guild.name + ".**")
            config_created = await sqlconfig.create_config(ctx.guild.id)
            if config_created:
                await ctx.send(":bookmark_tabs: **Created config entry!**")
            else:
                await ctx.send(":x: **Unable to create config entry. Please contact the bot developers.**")
                return
            config_cached = await server_config.get_config(ctx.guild)
            if config_cached is not None:
                await ctx.send(":computer: **Loaded config into memory.**")
            await ctx.send(":white_check_mark: **Setup completed! Please use the `config` command to set your "
                           "verified role, minimum rank requirement and more.**")

    @commands.command(aliases=['vc', 'viewconf'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def viewconfig(self, ctx: Context):
        cfg = await server_config.get_config(ctx.guild)
        if cfg is not None:
            await ctx.send(embed = cfg.get_embed())
        else:
            await ctx.send(":x: **No config exists for this server. Please use the `setup` command.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context, *args):
        await config.config(ctx, args)

    @commands.command(aliases=['mv', 'manver'])
    @commands.guild_only()
    @is_rl_or_higher()
    async def manualverify(self, ctx: Context, *args):
        await manual_verify.manual_verify(ctx, self.bot, args)

    @commands.command(aliases=['sl'])
    @commands.guild_only()
    @is_rl_or_higher()
    async def suspendlist(self, ctx: Context):
        try:
            data = None
            with open("suspend.log", 'r+') as sl:
                data = json.loads(sl.read())
                sl.close()

            embed=Embed(title="Suspended Users", description="Current suspended users")
            if not data is None:
                for uid in data:
                    user = ctx.message.guild.get_member(int(uid))
                    embed.add_field(name="{}".format(user.nick), value="User:**<@!{}>** \n Suspended by: **<@!{}>** \n For Duration **{}** mins".format(user.id, data[uid]['suspender'],data[uid]['dur']), inline=True)
            embed.set_footer(text="Space Travel Dungeons")
            await ctx.send(embed=embed)
        except Exception as e:
            embed=Embed(description="**.suspendlist -> lists all currently suspended players", color=0x2ffef7)
            embed.set_footer(text="Space Travel Dungeons")
            await ctx.send(embed=embed)
            print(e)

async def on_reaction_add(reaction: Reaction, user: User):
    pass

def setup(client):
    client.add_cog(ModerationCommands(client))
