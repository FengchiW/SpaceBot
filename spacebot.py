# Spacebot

import os
from discord.ext.commands import Bot
import discord
import time
import sqlite3
import sql
import verify
from cmd import get_stats, get_status, get_leaderboard

#DONT LOOK!
DISCORD_TOKEN="NzYxMDE3MzY5NTYwMzUwNzIw.X3Uepw.fqca_3Vc2l98bdLmrfElBy2FWC4"

TOKEN = DISCORD_TOKEN

# Keep all intents; get everything hehe.
intents = discord.Intents.all()
client = Bot(command_prefix="!", intents=intents)

# All the guilds this bot belongs too
servers = []


def get_channel_by_name(server, name):
    for c in server.channels:
        if c.name == name:
            return c

def hasperms(member):
    for role in member.roles:
        if role.name in ["Admins", "Owner", "Moderators", "Leader", "Head Leader", "Security"]:
            return True
    else:
        return False

@client.event
async def on_ready():
    global servers
    sql.connect()
    print(f'{client.user.name} has connected to Discord! Version 1.2')
    for guild in client.guilds:
        servers.append(guild)

@client.event
async def on_member_join(member):
    pass

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        pass
    elif message.content == "" or message.content == None:
        pass
    elif message.content.upper().find('BOOB') != -1:
        await message.channel.send("```%s Sorry I can't give you something you'll never get. However, you may fondle your own.```" % (message.author.display_name))
    elif message.content == "<:YamaKing:762132762018709504>":
        if message.channel == get_channel_by_name(message.guild, "│yamaking-chat"):
            await message.channel.send("<:YamaKing:762132762018709504>")
    elif message.content[0] == '!' or message.content[0] == '?':
        content = message.content.split(" ")
        cmd = content[0].upper()
        member_user = None

        if cmd == '?STATS':
            if len(content) > 1:
                await message.channel.send(embed = get_stats(content[1][3:-1]))
            else:
                await message.channel.send(embed = get_stats(message.author.id))
        elif cmd == '!VERIFY':
            print("Verifying")
            member_user = message.author
            sql.add_user(member_user.name, member_user.id)

            embed=discord.Embed(title="Thank you for verifying your account on Space Travel Dungeon")
            embed.set_author(name="Space Ship Bot")
            embed.add_field(name="Your verification code is", value="%s"%(sql.fetch_user(member_user.id)[1]), inline=False)
            embed.add_field(name="Add the code to one of your realmeye lines", value="then type ```!confirm { ign }```", inline=True)

            dm_channel = await member_user.create_dm()

            await dm_channel.send(embed=embed)

            await message.delete()
        elif cmd == '!CONFIRM':
            if len(message.content.split(" ")) > 1:
                server = None
                member_user = None
                for guild in client.guilds:
                    for member in guild.members:
                        if int(message.author.id) == int(member.id):
                            server = guild
                            member_user = member
                    if member_user == None:
                        print("ERR Cant find user")

                print(server.id, message.author.id)
                dm_channel = message.author.dm_channel
                ign = message.content.split(" ")[1]
                eventcode = verify.verify(ign, sql.fetch_user(message.author.id)[1])
                if eventcode == "SUCCESS":
                    guild_roles = server.roles
                    member_role = None

                    sql.changeName(message.author.id, ign)

                    for role in guild_roles:
                        if role.name == "Member": # MEMBER ROLE NAME
                            member_role = role

                    new_nick = message.content.split(" ")[1]
                
                    try:
                        await member_user.add_roles(member_role)
                    except Exception as e:
                        print("Cant add role", e)
                    try:
                        await member_user.edit(nick = new_nick)
                    except Exception:
                        print("Can't Change this user's nickname or nick")

                    await dm_channel.send("```Success```")
                    await get_channel_by_name(server, "│verification-logs").send("```%s | has been verified```" % (message.author.name))
                else:
                    await dm_channel.send("```Sorry, Try again Error: %s```" % (eventcode))
                    await get_channel_by_name(server, "│verification-logs").send("```%s | has Failed to verify Reson: %s ```" % (member_user.name, eventcode))
        elif cmd == '!BOTSTATUS':
            pass
        elif cmd == '!LEADERBOARD':
            await message.channel.send(embed = get_leaderboard())

        for member in message.guild.members:
                if int(message.author.id) == int(member.id):
                    member_user = member
        print(hasperms(member_user))
        if hasperms(member_user):
            if cmd == '!LOGKEY' or cmd == '!LK':
                print("Logging key")
                sql.logkey(int(content[1][3:-1]), int(content[2]))
                await message.delete()
            elif cmd == '!MKDB':
                await message.channel.send("RE-BUILDING")
                for member in message.guild.members:
                    sql.add_user(member.display_name, member.id)
            elif cmd == '!LOGVILE' or cmd == '!LV':
                print("Logging Vile")
                sql.logvile(int(content[1][3:-1]), int(content[2]))
                await message.delete()
            elif cmd == '!LOGRUNE' or cmd == '!LR':
                print("Logging Rune")
                sql.logrune(int(content[1][3:-1]), int(content[2]))
                await message.delete()
            elif cmd == '!MV' or cmd == '!MANVER':
                print("Man Ver")
                server = message.guild
                content = message.content.split(" ")
                member_user = None
                guild_roles = server.roles

                for member in server.members:
                    if int(member.id) == int(content[1][3:-1]):
                        member_user = member
                if member_user == None:
                    print("ERR Cant find user")

                member_role = None

                for role in guild_roles:
                    if role.name == "Member": # MEMBER ROLE NAME
                        member_role = role

                new_nick = content[2]
                
                print("ADDED USER TO DATABASE")
                sql.add_user(new_nick, member_user.id)

                try:
                    await member_user.add_roles(member_role)
                except Exception as e:
                    print("Cant add role", e)
                try:
                    await member_user.edit(nick = new_nick)
                except Exception:
                    print("Can't Change this user's nickname or nick")

                await get_channel_by_name(server, "│verification-logs").send("```%s | has been manually verified by %s```" % (new_nick, message.author.name))

                await message.delete()
            elif cmd == '!HC' or cmd == '!HEADCOUNT':
                pass
client.run(TOKEN)