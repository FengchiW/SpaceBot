from discord import Emoji, Guild
from discord.utils import get
from emojis import encode, decode


def get_emoji(string: str, guild: Guild):
    custom = get(guild.emojis, name=string)
    builtin = encode(string)
    return custom if custom is not None else builtin
