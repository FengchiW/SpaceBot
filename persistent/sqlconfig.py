import simplejson as json
from util.constants import SERVER_CONFIG_DB, SQL_CONFIG_DUNGEON_ROLES, SQL_CONFIG_EMOJI_DATA, \
    SQL_CONFIG_RAID_CHANNEL_ID, SQL_CONFIG_RANK_MINIMUM, SQL_CONFIG_GID, SQL_CONFIG_VERIFIED_ROLE_ID

async def create_suspend_list(gid):
    with open("suspended.json", 'r+') as configfile:
        data = json.loads(configfile.read())
        if gid in data:
            print("A config already exists for server with ID " + str(gid) + ".")
            configfile.close()
            return False
        else:
            data[str(gid)] = {}
            configfile.seek(0)
            json.dump(data, configfile)
            configfile.close()
            print("Executed config creation query for guild " + str(gid) + ".")
            return True

async def create_config(gid):
    with open(SERVER_CONFIG_DB, 'r+') as configfile:
        data = json.loads(configfile.read())
        if gid in data:
            print("A config already exists for server with ID " + str(gid) + ".")
            configfile.close()
            return False
        else:
            data[str(gid)] = {
                SQL_CONFIG_GID: gid,
                SQL_CONFIG_RANK_MINIMUM: 0,
                SQL_CONFIG_VERIFIED_ROLE_ID: 0,
                SQL_CONFIG_RAID_CHANNEL_ID: 0,
                SQL_CONFIG_DUNGEON_ROLES: "",
                SQL_CONFIG_EMOJI_DATA: {}
            }
            configfile.seek(0)
            json.dump(data, configfile)
            configfile.close()
            await create_suspend_list(gid)
            print("Executed config creation query for guild " + str(gid) + ".")
            return True


async def fetch_config(gid):
    print("Fetching Server config...")
    with open(SERVER_CONFIG_DB, 'r') as configfile:
        data = json.loads(configfile.read())
        if data is None:
            configfile.close()
            return None
        if str(gid) in data:
            configfile.close()
            print("Success! Fetched Config for %s" % (gid))
            return data[str(gid)]
        else:
            configfile.close()
            print("No config found for server %s" % (gid))
            return None


async def update_config(gid, column: str, value) -> bool:
    if await fetch_config(gid) is None:
        print("Guild with ID %s has no config set up." % gid)
        return False
    else:
        with open(SERVER_CONFIG_DB, 'r+') as configfile:
            data = json.loads(configfile.read())
            data[str(gid)][column] = value
            configfile.seek(0)
            json.dump(data, configfile)
            configfile.close()
        return True
