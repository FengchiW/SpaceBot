from discord.ext import commands
from discord.ext.commands import Context
from util.permissions import is_rl_or_higher, is_staff, is_admin, is_security

class DevCommands(commands.Cog):
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

def setup(client):
    client.add_cog(DevCommands(client))
