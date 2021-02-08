from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context
from persistent import sql, server_config, sqlconfig
from util import constants
from cogs.moderation import config, manual_verify, staff_verify
from util.permissions import is_rl_or_higher, is_staff, is_admin, is_security
import simplejson as json
from discord import Embed
from discord.utils import get
import re

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
                    if not user is None:
                        embed.add_field(name="{}".format(user.display_name), value="User:**<@!{}>** \n Suspended by: **<@!{}>** \n For Duration **{}** mins".format(user.id, data[uid]['suspender'],data[uid]['dur']), inline=True)
            embed.set_footer(text="Space Travel Dungeons")
            await ctx.send(embed=embed)
        except Exception as e:
            embed=Embed(description="**.suspendlist -> lists all currently suspended players", color=0x2ffef7)
            embed.set_footer(text="Space Travel Dungeons")
            await ctx.send(embed=embed)
            print(e)
    
    @commands.command(aliases=['rs', 'registerstaff'])
    @commands.guild_only()
    @is_staff()
    async def register(self, ctx: Context, *args):
        await staff_verify.rs(ctx, args)
    
    @commands.command(aliases=['noquota'])
    @commands.guild_only()
    @is_staff()
    async def idontlead(self, ctx: Context, name = None):
        staffinfo  = get(ctx.message.guild.channels, id=761788719685435404)
        uid = ctx.author.id
        if not name is None:
            uid = int(re.sub('[<!@>]', '', name))
        await sql.idontlead( uid )
        embed=Embed(title="No Quota", description="Warning, <@!%s> id: <@!%s> says that he is should not have a quota."% (ctx.message.author.id, uid))
        msg = await staffinfo.send(embed=embed)
        await ctx.message.add_reaction("✔")

    @commands.command(aliases=['ss'])
    @is_staff()
    async def staffstats(self, ctx: Context, name=None):
        uid = ctx.author.id
        if not name is None:
            uid = int(re.sub('[<!@>]', '', name))
        print(name, uid)
        
        user = await sql.fetch_staff(uid)

        if user is None:
            await sql.addstaff(uid, 1, 0)

        user = await sql.fetch_staff(uid)

        requiredpnts = 0

        if user['rolelevel'] == 1:
            requiredpnts = 40
        elif user['rolelevel'] == 0:
            requiredpnts = 0
        else:
            requiredpnts = 50

        embed=Embed    (title="Staff Stats",       description="<@!%s>" % (uid))
        embed.add_field(name="O3's led: ",         value="%s"   % (user['o3']),               inline=True)
        embed.add_field(name="Halls led: ",        value="%s"   % (user['halls']),            inline=True)
        embed.add_field(name="Exaltations Led: ",  value="%s"   % (user['exalt']),            inline=True)
        embed.add_field(name="Misc Led: ",         value="%s"   % (user['other']),            inline=True)
        embed.add_field(name="Weekly Points: ",    value="%s"   % (user['points']),           inline=True)
        embed.add_field(name="Required Points: ",  value="%s"   % requiredpnts,               inline=True)
        embed.add_field(name="All Time Points: ",  value="%s"   % (user['alltime']),          inline=True)
        embed.add_field(name="Pot Ratio: ",        value="%s"   % (user['potratio']),         inline=True)
        embed.add_field(name="Failed Runs: ",      value="%s"   % (user['failed']),           inline=True)
        embed.add_field(name="On Leave: ",         value="%s"   % (user['leave']),            inline=True)
        embed.add_field(name="Warnings: ",         value="%s"   % (user['warn']),             inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['rl!'])
    @is_staff()
    async def imanrl(self, ctx: Context):
        uid = ctx.author.id
        await sql.imanrl(int(uid))
        await ctx.send('Bet.')

    @commands.command()
    @is_admin()
    async def resetstaff(self, ctx):
        await sql.reset_all()
        await ctx.send('Okay, lazy boi')

    @commands.command()
    @is_security()
    async def purge(self, ctx, amt = 1):
        if(amt > 20):
            amt = 1
            ctx.send("you can't purge more than 20 msg")
        staffinfo  = get(ctx.message.guild.channels, id=805617569054326795)
        await ctx.channel.purge(limit=amt)
        await staffinfo.send('`<@!%s> Cleared %s message(s) from %s`' % (ctx.message.author.id, amt, ctx.message.channel.name))
    
    @commands.command()
    @is_admin()
    async def rollover(self, ctx):
        data = await sql.rollover()

        for user in data:
            member = ctx.message.guild.get_member(int(user[0]))
        await ctx.send('done')
    
    @commands.command(aliases = ['sleaderboard'])
    async def slb(self, ctx: Context, req = None):
        if req == None:
            req = "Points"
            sl = await sql.get_staff_list("POINTS")
        elif req.lower() == "o3":
            req = "O3's Led"
            sl = await sql.get_staff_list("O3_LED")
        elif req.lower() == "halls":
            req = "Halls's Led"
            sl = await sql.get_staff_list("HALLS_LED")
        elif req.lower() == "other":
            req = "Other dungeons's Led"
            sl = await sql.get_staff_list("OTHER_LED")
        else:
            req = "Points"
            sl = await sql.get_staff_list("POINTS")
        

        embed=Embed(title="Staff Leaderboard", description="Ranked by %s" % (req))
        feildtext = ""
        for staff in sl:
            feildtext += "**<@!%s>**: **%s** %s! \n" % (staff[0], staff[1], req)

        embed.add_field(name = "========================", value=feildtext, inline=False)
        await ctx.send(embed=embed)
    
async def on_reaction_add(reaction: Reaction, user: User):
    pass

def setup(client):
    client.add_cog(ModerationCommands(client))
