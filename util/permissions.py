
import discord
from discord.ext import commands

def is_bot_owner():
    def predicate(ctx):
        return ctx.author.id == ctx.bot.owner_id
    return commands.check(predicate)

def is_staff():
    def predicate(ctx):
        return any(role.name in ["Admins", "Trial Raid Leader", "Owner", "Moderators", "Halls Leader", "Head Leader",  "Oryx Leader", "Exalted Leader",  "Security", "Officer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_rl_or_higher():
    def predicate(ctx):
        return any(role.name in ["Admins", "Halls ARL", "Oryx ARL", "Owner", "Moderators", "Halls Leader", "Head Leader",  "Oryx Leader", "Exalted Leader",  "Security", "Officer", "Event Organizer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_security():
    def predicate(ctx):
        return any(role.name in ["Admins", "Owner", "Moderators", "Security", "Officer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        return any(role.name in ["Admins", "Owner", "Bot Maker"] for role in ctx.author.roles)
    return commands.check(predicate)
