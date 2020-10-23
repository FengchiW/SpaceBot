from typing import List
from discord import Emoji



class ServerConfig:
    def __init__(self):
        self.verified_role_id: int = 0
        self.raid_channel: int = 0
        self.dungeon_roles: List = []

    def load_from_file(self, config_file):
        pass


class DungeonRole:
    def __init__(self, role_id: int, name: str, icon: Emoji):
        self.role_id: int = role_id
        self.dungeon_name: str = name
        self.dungeon_icon: Emoji = icon
