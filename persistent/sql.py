import mysql.connector
from util import constants
from mysql.connector import Error, MySQLConnection
from typing import Dict
from util.logging import log, LogLevel
from . import sqlconfig

connection: MySQLConnection = None


# User data table format:
# UID    VERIFIED IGN ALT O3       RUNS     KEY_POPS RUNES      VIALS      POINTS
# bigint str      str str smallint smallint smallint smallint   smallint   int
# 0      1        2   3   4        5        6        7          8          9

# Server config table format:
# GID    MIN_RANK VERIFIED_ROLE_ID RAID_CHANNEL_ID DUNGEON_ROLES
# bigint smallint bigint           bigint          json
# 0      1        2                3               4
# Raiding roles take the following format: [dungeon name]_|_[role id]_|_[associated emoji (for reactions, etc)}

async def connect() -> bool:
    """Connects to the SQL server. Returns True if connection was successful,
    False if not."""
    global connection
    connection = None
    try:
        # initialize connection
        connection = mysql.connector.connect(
            host='li2140-92.members.linode.com',
            port=3306,
            database='STD',
            user='<hidden>',
            password='<hidden>'
        )
        await log("Successfully connected to the SQL server.")
        await log("Checking config table...")
        return True
    except Error as e:
        await log("Something went wrong connecting to the SQL server.", LogLevel.ERROR)
        await log(e.__str__(), LogLevel.DEBUG)
        return False


async def add_user(gid, uid, ign):
    """Attempts to add a user with id uid to server with id gid. Returns False if
    not connected or the user is already in the table, True if the user was successfully
    added."""
    if connection is None:
        await log("Please connect to the SQL server before attempting to insert data.", LogLevel.ERROR)
        return False
    if await fetch_user(gid, uid) is not None:
        await log("User " + uid + " already exists in the database.", LogLevel.WARN)
        return False
    try:
        cursor = connection.cursor()
        query = "INSERT INTO `%(guild)s` VALUES (%(user)s, %(verified)s, %(ign)s, 'NONE', 0, 0, 0, 0, 0, 0)"
        cursor.execute(query, {'guild': gid,
                               'verified': "True",
                               'user': uid,
                               'ign': ign})
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        await log("An error occurred while adding a user.", LogLevel.ERROR)
        await log(e.__str__(), LogLevel.DEBUG)
        return False


async def fetch_user(gid, uid):
    if connection is None:
        await log("Please connect to the SQL server before attempting to make queries.", LogLevel.ERROR)
        return None
    try:
        cursor = connection.cursor(buffered=True)
        query = "SELECT DISTINCT * FROM `%(guild)s` WHERE " + constants.SQL_UID + " = %(user)s"
        cursor.execute(query, {
            'guild': gid,
            'user': uid
        })
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return None

        out: Dict = {
            constants.SQL_UID: data[0],
            constants.SQL_VERIFIED: data[1],
            constants.SQL_IGN: data[2],
            constants.SQL_ALT: data[3],
            constants.SQL_O3: data[4],
            constants.SQL_RUNS: data[5],
            constants.SQL_KEY_POPS: data[6],
            constants.SQL_RUNES: data[7],
            constants.SQL_VIALS: data[8],
            constants.SQL_POINTS: data[9]
        }
        
        return out
    except Exception as e:
        await log("An error occurred when attempting to fetch user with UID " + str(uid) + ".", LogLevel.ERROR)
        connection.reconnect(attempts=3, delay=0)
        await log(e.__str__(), LogLevel.DEBUG)
        return None


async def update_user(uid, column, change, gid):
    try:
        if await fetch_user(gid, uid) is None:
            await add_user("Null", gid, uid)
        if not connection is None:
            cursor = connection.cursor()

            sql = "UPDATE `%(guild)s` SET {} = %(value)s WHERE UID = %(user)s".format(
                column)  # This is fine because Colunm modified is constant

            print(sql % {'guild': gid,
                         'value': change,
                         'user': uid})
            cursor.execute(sql, {'guild': gid,
                                 'value': change,
                                 'user': uid})
            connection.commit()
            cursor.close()
            return "Edited User %s %s %s" % (column, change, uid)
        else:
            print("Something went wrong")
            return "Failed to add User"
    except Error as e:
        print("Update User Fail", e)
        return "ERROR"

async def log_changes(uid, gid, change, amount, points):
    try:
        if await fetch_user(gid, uid) is None:
            await add_user("Null", gid, uid)
        if not connection is None:
            cursor = connection.cursor()

            sql = "UPDATE `%(guild)s` SET {} = {} + %(value)s WHERE UID = %(user)s".format(
                change, change)  # This is fine because Colunm modified is constant

            cursor.execute(sql, {'guild': gid,
                                 'value': amount,
                                 'user': uid})
            connection.commit()
            cursor.close()
            return "Edited User %s %s %s" % (change, amount, uid)
        else:
            print("Something went wrong")

            return "Failed to add User"
    except Error as e:
        print("Update User Fail", e)
        return "ERROR"


async def drop_table(table_name):
    if connection is None:
        await log("Please connect to the SQL server before attempting to drop the server config table.", LogLevel.ERROR)
        return False
    try:
        cursor = connection.cursor(buffered=True)
        query = "DROP TABLE %(table)s"
        cursor.execute(query, {
            "table": table_name
        })
        connection.commit()
        cursor.close()
    except Exception as e:
        await log("Error encountered while attempting to drop table %s from SQL server." % table_name, LogLevel.ERROR)
        await log(e.__str__(), LogLevel.DEBUG)
