from discord.ext import commands, tasks
from discord import Intents, User, Reaction, Message, TextChannel
from discord.ext.commands import CommandNotFound, Context, CommandInvokeError
from emojis import decode
from discord import Embed

from discord.utils import get

from persistent import server_config, sql
from util.logging import log, LogLevel
import asyncio
import simplejson as json

# settings.py
from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime, timedelta

LIVETOKEN = os.getenv("LIVETOKEN")
DEVTOKEN = os.getenv("DEVTOKEN")

# dev token, please start using environment variables...
#Different token
DISCORD_TOKEN = LIVETOKEN


TOKEN = DISCORD_TOKEN
VERSION = "0.2.7"
COMMAND_PREFIX = "."

intents = Intents.all()

client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
client.remove_command('help')

@tasks.loop(seconds = 120)
async def st():
    while True:
        with open("suspend.log", 'r+') as sl:
            data = json.loads(sl.read())
            await log(data)
            guild = get(client.guilds, id=522815906376843274)
            suspended_role = get(guild.roles, id=522847611649130506)
            mr = get(guild.roles, id=522817975091462147)
            dellist = []
            for uid in data:
                member = await guild.fetch_member(uid)
                if data[uid]['dur'] <= 0:
                    print("unsupending user")
                    if member is None:
                        print("Error Null Member")
                    else:
                        try:
                            await member.remove_roles(suspended_role)
                            if suspended_role is not None:
                                await member.add_roles(mr)
                                logchannel = get(guild.channels, id=761788719685435404)
                                suschannel = get(guild.channels, id=763644055536009216)
                                embed=Embed(title="User Unsuspended", description="**%s**, He has served his time \n Unsuspender: **SpaceBot**" % (member.display_name))

                                await suschannel.send(embed=embed)
                                await logchannel.send(embed=embed)
                        except Exception as e:
                            print(e)
                    dellist.append(uid)
                else:
                    data[uid]['dur'] = data[uid]['dur'] - 1
            for uid in dellist:
                data.pop(uid, None)
            sl.seek(0)
            json.dump(data, sl)
            sl.truncate()
            sl.close()

@tasks.loop(seconds = 604800)
async def pt():
    data = await sql.rollover()
    guild = get(client.guilds, id=522815906376843274)

    for user in data:
        member = guild.get_member(int(user[0]))
        dm_channel = await member.create_dm()

        e = Embed(
            title="Inactivity Notification", 
            description='''
            **You failed to meet quota this week.**
            Your weekly quota is: **%s** points, but you only had **%s** points.
            If this happens twice in a row without explaining your reasoning to upper staff, you will be demoted for inactivity.
            ''' % (40, user[1]), 
            color=0xdb021c)
        e.set_footer(text="Space Travel Dungeons", icon_url = "https://cdn.discordapp.com/attachments/751589431441490082/764948382912479252/SPACE.gif")
        await dm_channel.send(embed = e)
    print("Rolling over")

@pt.before_loop
async def bpt():
    hour = 23
    minute = 55
    await client.wait_until_ready()
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)
    await asyncio.sleep((future-now).seconds)

@client.event
async def on_ready():
    await log(f'{client.user.name} v{VERSION} has connected to Discord!')
    await log("Attempting connection to SQL server...")
    await sql.connect()
    # Loads config for guilds the bot is currently a member of.
    await log("Loading config for connected guilds.")
    st.start()
    pt.start()
    for guild in client.guilds:
        cfg = await server_config.get_config(guild)
        if cfg is not None:
            await log("Loaded config for guild " + guild.name + " with id " + str(guild.id) + ".")


@client.event
async def on_message(message: Message):
    user: str = f"{message.author.name}#{message.author.discriminator}"
    channel = "DMs"
    if message.guild is not None:
        channel = f"(guild {message.guild.name} with id {message.guild.id})"
    msg: str = message.content
    if msg.startswith(COMMAND_PREFIX):
        await log(f"{user} issued command {msg} in {channel}.")
        await client.process_commands(message)


@client.event
async def on_command_error(ctx: Context, error):
    if isinstance(error, CommandNotFound):
        pass
        #await ctx.send(f":x: **Command `{ctx.message.content.split()[0].replace(COMMAND_PREFIX, '')}` not found.**")
    #elif isinstance(error, CommandInvokeError):
    #    await ctx.send(":x: **Unable to invoke command.** Ensure you allow direct messages for server members.", delete_after=10)
    else:
        await log("An exception occurred while executing this command.", LogLevel.WARN)
        await log(error.__str__())


@client.event
async def on_member_join(member):
    pass


'''
@client.event
async def on_reaction_add(reaction: Reaction, user: User):
    if reaction.message.author.id != client.user.id:
        return
    if decode(reaction.emoji) == ":egg:":
        print("egg detected")
    for cog in client.extensions.values():
        listener_method = getattr(cog, "on_reaction_add")
        if listener_method is not None:
            try:
                await listener_method(reaction, user)
            except Exception as e:
                # exception should only occur if there's no such method -
                # ignore it, that's fine
                continue
'''

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename != '__init__.py':
            print(f"Loading cog from {filename}.")
            client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
