from discord import Reaction, User
from discord.ext import commands
from discord.ext.commands import Context
from persistent import sql, server_config, sqlconfig
from util import constants
from cogs.moderation import config, manual_verify, staff_verify
from util.permissions import is_rl_or_higher, is_staff, is_admin, is_security
from discord import Embed
from discord.utils import get
import re

developers = [218169424132177920, 235241036388106241]


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        pass

    @commands.command()
    @is_security()
    async def purge(self, ctx, amt = 1):
        if(amt > 20):
            amt = 1
            ctx.send("you can't purge more than 20 msg")
        staffinfo  = get(ctx.message.guild.channels, id=761788719685435404)
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
        elif req.lower() == "alltime":
            req = "All time points"
            sl = await sql.get_staff_list("ALLTIME")
        elif req.lower() == "pot":
            req = "Pot Ratio"
            sl = await sql.get_staff_list("POT_RATIO", "ASC")
        else:
            req = "Points"
            sl = await sql.get_staff_list("POINTS")
        

        embed=Embed(title="Staff Leaderboard", description="Ranked by %s" % (req))
        feildtext = ""
        for staff in sl:
            feildtext += "**<@!%s>**: **%s** %s! \n" % (staff[0], staff[1], req)

        embed.add_field(name = "========================", value=feildtext, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def aq(self, ctx: Context):
        tomake = [
        {
            "role": "Moderation Branch Hierarchy",
            "color": 0x000000,
            "desc": "**<@&761313993159475280> < <@&780306791212122153> < <@&522816654091223051>**"
        },
        {
            "role": "Raid Leader Branch",
            "color": 0x000000,
            "desc": "**<@&790331735631593472> = <@&522817272616583181> < <@&790743719112343553> = <@&780543201333215295> < <@&779512163923525672> = <@&780515270446940161> < <@&765649870979596299> < <@&761211992438472744> < <@&522816654091223051>**"
        }
        ]

        for role in tomake:
            embed=Embed(
                title="%s" % (role["role"]), 
                description="%s"% (role["desc"]),
                color=role["color"])
            embed.set_footer(text="Space Travel Dungeons", icon_url="https://cdn.discordapp.com/attachments/751589431441490082/764948382912479252/SPACE.gif")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(ModerationCommands(client))
