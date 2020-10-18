from discord.ext import commands

async def is_Leader_or_higher(ctx):
    return any(role.name in ["Admins", "Owner", "Moderators", "Leader", "Head Leader", "Security"] for role in ctx.author.roles)

async def is_Mod_or_higher(ctx):
    return any(role.name in ["Admins", "Owner", "Moderators", "Security"] for role in ctx.author.roles)

async def is_admin(ctx):
    return any(role.name in ["Admins", "Owner"] for role in ctx.author.roles)