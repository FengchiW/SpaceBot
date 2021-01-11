from discord import Guild, Emoji, Embed
from persistent import sqlconfig
from util import constants

active_configs = dict()


async def create_config(guild: Guild) -> bool:
    """Creates a ServerConfig for the guild in question."""
    # don't allow config creation if it exists already
    if await get_config(guild) is not None:
        print("Guild " + guild.name + " with id " + guild.id + " already in config cache.")
        return False
    cfg = ServerConfig(guild)
    active_configs[guild.id] = cfg
    return True

async def get_config(guild: Guild) -> 'ServerConfig':
    # try cache first
    cfg = active_configs.get(guild.id)
    if cfg is None:
        # try SQL if not found in cache
        cfg = await from_sql(guild)
        if cfg is not None:
            # If the config was found in SQL, load it into cache to reduce strain on SQL server
            active_configs[guild.id] = cfg
        else:
            print("No config available for guild with id " + str(guild.id) + ".")
    return cfg


async def from_sql(guild: Guild) -> 'ServerConfig':
    data = await sqlconfig.fetch_config(guild.id)
    if data is None:
        return None
    cfg = ServerConfig(guild)
    cfg.min_rank = data[constants.SQL_CONFIG_RANK_MINIMUM]
    cfg.verified_role_id = data[constants.SQL_CONFIG_VERIFIED_ROLE_ID]
    cfg.raiding_channel_id = data[constants.SQL_CONFIG_RAID_CHANNEL_ID]
    return cfg


async def update_sql(guild: Guild):
    cfg = await get_config(guild)
    if cfg is None:
        print("Can't write a nonexistent config.")
    else:
        print("Updating config in database for guild %s with ID %s." % (guild.name, guild.id))
        current_cfg = await from_sql(guild)
        # Only update things that have changed.
        if current_cfg.verified_role_id != cfg.verified_role_id:
            print("Verified role ID has changed, updating.")
            await sqlconfig.update_config(guild.id, constants.SQL_CONFIG_VERIFIED_ROLE_ID, cfg.verified_role_id)
        if current_cfg.min_rank != cfg.min_rank:
            print("Minimum rank requirement has changed, updating.")
            await sqlconfig.update_config(guild.id, constants.SQL_CONFIG_RANK_MINIMUM, cfg.min_rank)
        if current_cfg.raiding_channel_id != cfg.raiding_channel_id:
            print("Raiding channel ID has changed, updating.")
            await sqlconfig.update_config(guild.id, constants.SQL_CONFIG_RAID_CHANNEL_ID, cfg.raiding_channel_id)

class ServerConfig:

    def __init__(self, guild: Guild):
        self.guild = guild
        self.verified_role_id = 0
        self.min_rank = 0
        self.raiding_channel_id = 0
        self.dungeon_roles = set()

    def get_embed(self):
        embed = Embed(title="ServerConfig for %s "%(self.guild.name), url="https://youtu.be/180hrQFK0-c",
                          description="Here are the current settings for the server, you can modify them but using ;config",
                          color=0x0062ff)
        embed.set_author(name=self.guild.name)
        embed.add_field(name="Verified role id:", value=self.verified_role_id, inline=False)
        embed.add_field(name="Minimum rank to verify:", value=str(self.min_rank), inline=False)
        embed.add_field(name="Raiding channel id:", value=self.raiding_channel_id, inline=False)
        embed.add_field(name="Dungeons", value="Soon", inline=False)
        return embed


class DungeonRole:
    def __init(self, dungeon_name: str, role_id: int, emoji: Emoji):
        self.dungeon_name = dungeon_name
        self.role_id = role_id
        self.emoji = emoji
