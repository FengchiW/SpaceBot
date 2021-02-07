
import discord
from discord.ext import commands

def is_bot_owner():
    def predicate(ctx):
        return ctx.author.id == ctx.bot.owner_id
    return commands.check(predicate)

def is_staff():
    def predicate(ctx):
        return any(role.name in ["Admin", "Event Organizer", "Trial Raid Leader", "Halls ARL", "Oryx ARL", "Owner", "Moderators", "Halls Leader", "Head Leader",  "Oryx Leader", "Exalted Leader",  "Security", "Officer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_rl_or_higher():
    def predicate(ctx):
        return any(role.name in ["Admin", "Event Organizer", "Halls ARL", "Oryx ARL", "Owner", "Moderators", "Halls Leader", "Head Leader",  "Oryx Leader", "Exalted Leader",  "Security", "Officer", "Event Organizer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_security():
    def predicate(ctx):
        return any(role.name in ["Admin", "Owner", "Moderator", "Security", "Officer"] for role in ctx.author.roles)
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        return any(role.name in ["Admin", "Owner", "Bot Dev"] for role in ctx.author.roles)
    return commands.check(predicate)
