from discord.ext.commands import Context
from emojis import encode

from util.embeds.config_embeds import config_embed
from persistent import server_config

confirmed_emoji = encode(":white_check_mark:")

options = { "verify-role": ("The ID of the role to assign to users who successfully verify.",
                           'verified_role_id', int),
            "min-rank": ("The minimum in-game rank a user must be to verify for this server.",
                        'min_rank', int),
            "raid-channel": ("The ID of the default channel to which headcounts and raid announcements are sent.",
                            'raiding_channel_id', int)}


async def config(ctx: Context, args):
    # pull the guild's config
    cfg = await server_config.get_config(ctx.guild)
    # don't let anyone configure anything so long as the guild hasn't been set up with its own SQL table et
    if cfg is None:
        await ctx.send(":x: **This server needs to be set up with `setup` before it can be configured.**")
        return
    if len(args) == 0:
        await ctx.send(embed=config_embed(options))
    else:
        config_var = args[0]
        if config_var == "add-dungeon":
            print("add dungeon code")
        if config_var not in options:
            await ctx.send(":x: **Unrecognized option: %s**" % config_var)
        elif len(args) == 1:
            await ctx.send(":question: **Please provide a value for this new config.**")
        else:
            value = args[1]
            attr = options[config_var][1]
            val_type = options[config_var][2]
            try:
                setattr(cfg, attr, val_type(value))
                await server_config.update_sql(ctx.guild)
                await ctx.message.add_reaction(confirmed_emoji)
            except ValueError:
                await ctx.send(":x: **This option only accepts arguments of type " + str(val_type) + ".**")
            except Exception as e:
                await ctx.send(":x: **An error occurred when attempting to set this option.")
                print(e)