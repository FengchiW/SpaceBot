
import discord
from discord.ext import commands

def is_bot_owner():
    def predicate(ctx):
        return ctx.author.id == ctx.bot.owner_id
    return commands.check(predicate)

def is_rl_or_higher():
    def predicate(ctx):
        return any(role.name in ["Admins", "Owner", "Moderators", "Halls Leader", "Head Leader",  "Oryx Leader", "Exalted Leader",  "Security", "Officer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_security():
    def predicate(ctx):
        return any(role.name in ["Admins", "Owner", "Moderators", "Security", "Officer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        return any(role.name in ["Admins", "Owner"] for role in ctx.author.roles)
    return commands.check(predicate)
