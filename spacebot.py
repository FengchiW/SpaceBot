# Spacebot
from discord.ext import commands
from discord import Intents
import discord
import os

#DONT LOOK! We should put this in env
DISCORD_TOKEN="NzY3MTA2NzYxMzc0Njk1NDQ1.X4tF2A.nQVZcSzDWsPFNvT8BRH9YmcI7W4"

TOKEN = DISCORD_TOKEN

# Keep all intents; get everything hehe.
intents = Intents.all()

client = commands.Bot(command_prefix=";", intents=intents)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

    await ctx.send("%s loaded" % (extension))

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

    await ctx.send("%s unloaded" % (extension))

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

    await ctx.send("%s reloaded" % (extension))

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord! Version 1.2')

@client.event
async def on_member_join(member):
    pass

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename != '__init__.py':
            client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)