from discord import Reaction, User, Embed
from discord.ext import commands
from discord.ext.commands import Context
from util.permissions import is_rl_or_higher
import simplejson as json

from discord import Guild, Member
from discord.utils import get
from util import constants
import time

import re

class SuspentionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['s'])
    @is_rl_or_higher()
    async def suspend(self, ctx: Context, *args):
        try:
            uid = re.sub('[<!@>]', '', args[0])
            dur = str(args[1])
            tdur = dur
            alreadysuspend = False
            if any(c.isalpha() for c in dur):
                t = int(dur[:-1])
                x = dur[-1]
                if x == "d":
                    x = 1440
                elif x == "h":
                    x = 60
                elif x == "m":
                    x = 1
                elif x == "x":
                    x = 100000
                dur = x * t
            reason = " ".join(args[2:])
            guild: Guild = ctx.guild
            member: Member = await guild.fetch_member(uid)
            if member is None:
                await ctx.send(":x: **Can't find this member.**")
                return
            # Fetch the server's config to get the verified role ID.
            suspended_role = get(guild.roles, id=522847611649130506) #761019155583336488 522847611649130506
            # Put the user in the DB if they're not there already, or just update their verification status.
            with open("suspend.log", 'r+') as sl:
                data = json.loads(sl.read())
                if uid in data:
                    alreadysuspend = True
                    await ctx.send(":x: **Member already suspended, time will be added to the suspension, if this was a mistake type ;s [user] [-duration].**")
                    data[uid]['dur'] = int(data[uid]['dur']) + int(dur)
                    tdur = int(data[uid]['dur']) + int(dur)
                else:
                    data[uid] = {}
                    data[uid]['dur'] = int(dur) 
                data[uid]['suspender'] = ctx.message.author.id
                sl.seek(0)
                json.dump(data, sl)
                sl.truncate()
                sl.close()
            # Then add the verified role and change their nickname.
            # todo: put this common code into a single function in verify.py
            mr = get(guild.roles, id=522817975091462147)
            await member.remove_roles(mr)
            if suspended_role is not None:
                await member.add_roles(suspended_role)

            suschannel = get(guild.channels, id=763644055536009216)
            logchannel = get(guild.channels, id=761788719685435404)

            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            if not alreadysuspend:
                embed=Embed(title="User Suspended", description="**<@%s>** Suspended for **%s**.\n Dunce Hat for you.\n Reason: %s,\n Suspender: **<@%s>**" % (member.id, tdur, reason, ctx.author.id), color=0xff4242)
                embed.set_footer(text=current_time)
                
                await member.send(embed=embed)
                await suschannel.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                embed=Embed(title="Suspension Extended", description="**<@%s>** is now suspended for **%s**.\n Dunce Hat for you.\n Reason: %s,\n Suspender: **<@%s>**" % (member.id, tdur, reason, ctx.author.id), color=0xff4242)
                embed.set_footer(text=current_time)
                
                await member.send(embed=embed)
                await suschannel.send(embed=embed)
                await logchannel.send(embed=embed)
            await ctx.message.add_reaction(constants.EMOJI_CONFIRM)
        except Exception as e:
            embed=Embed(description="**.suspend\n**     Suspend Command.\n     **Usage:** `.suspend <@ user> <length> <reason>`\n     **<@ user>:** a mention of the user.\n     **<length>** The length of time, in `m, h, or d`. E.g. 2d, 3h, 10m.\n     **<reason>** The reason for suspension. Please be specific.\n     _Example:_ `.suspend @Daryl 2d being too cute for the server.`", color=0x2ffef7)
            embed.set_footer(text="Space Travel Dungeons")
            await ctx.send(embed=embed)
            print("Error Somewhere.", e)
    
    @commands.command(aliases=['us'])
    @is_rl_or_higher()
    async def unsuspend(self, ctx: Context, *args):
        try:
            # prune extraneous symbols from mentions
            uid = re.sub('[<!@>]', '', args[0])
            reason = None
            if len(args) > 1:
                reason = " ".join(args[1:])
            guild: Guild = ctx.guild
            member: Member = await guild.fetch_member(uid)
            if member is None:
                await ctx.send(":x: **Can't find this member.**")
                return

            # Fetch the server's config to get the verified role ID.
            suspended_role = get(guild.roles, id=522847611649130506) #761019155583336488 522847611649130506
            # Put the user in the DB if they're not there already, or just update their verification status.
            with open("suspend.log", 'r+') as sl:
                data = json.loads(sl.read())
                data.pop(uid, None)
                sl.seek(0)
                json.dump(data, sl)
                sl.truncate()
                sl.close()
            # Then add the verified role and change their nickname.
            # todo: put this common code into a single function in verify.py
            try:
                mr = get(guild.roles, id=522817975091462147)
                await member.remove_roles(suspended_role)
                if suspended_role is not None:
                    await member.add_roles(mr)
            except Exception as e:
                print(e)
            
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            logchannel = get(guild.channels, id=761788719685435404)
            suschannel = get(guild.channels, id=763644055536009216)
            embed=Embed(title="User Unsuspended", description="**<@%s>**,\n Unsuspender: **<@%s>**, \n Reason: %s" % (member.id, ctx.author.id, reason), color=0x33bc01)
            embed.set_footer(text=current_time)

            await member.send(embed=embed)
            await logchannel.send(embed=embed)
            await suschannel.send(embed=embed)
            await ctx.message.add_reaction(constants.EMOJI_CONFIRM)
        except Exception as e:
            embed=Embed(description="**.unsuspend\n** Unsuspend Command\n. **Usage:** `.unsuspend <@ user> <reason>`\n **<@ user>:** a mention of the user.\n **<reason>** The reason for unsuspension.\n _Example:_ `.unsuspend @Daryl being too cute for the server.", color=0x2ffef7)
            embed.set_footer(text="Space Travel Dungeons")
            await ctx.send(embed=embed)
            print(e)



def setup(client):
    client.add_cog(SuspentionCommands(client))
