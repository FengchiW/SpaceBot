import mysql.connector
from util import constants
from mysql.connector import Error, MySQLConnection
from typing import Dict
from util.logging import log, LogLevel
from . import sqlconfig

# settings.py
from dotenv import load_dotenv
load_dotenv()

import os

DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")
DBUSER = os.getenv("DBUSER")
DBPSW  = os.getenv("DBPSW")

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
            host=DBHOST,
            port=DBPORT,
            database='STD',
            user=DBUSER,
            password=DBPSW
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


async def fetch_leaderboard(gid, uid, sortby=constants.SQL_POINTS):
    if connection is None:
        await log("Please connect to the SQL server before attempting to make queries.", LogLevel.ERROR)
        return None
    try:
        cursor = connection.cursor(buffered=True)
        query = "SELECT * FROM `%(guild)s` ORDER BY %(sort)s DESC"
        tempquery = "SELECT * FROM `%s` ORDER BY POINTS DESC" % (gid)
        cursor.execute(tempquery)

        data = cursor.fetchmany(10)
        cursor.close()
        if data is None:
            return None

        out = []
        for row in data:
            out.append([row[2], row[9]])
        
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

async def log_run(uid, t, r = 0, p = 0):
    try:
        if await fetch_staff(uid) is None:
            await addstaff(addstaff, 0, -100)
        if not connection is None:
            cursor = connection.cursor()
            sql = ""
            if t == 0:
                sql = "UPDATE std_staff SET HALLS_LED = HALLS_LED + %(runs)s, POINTS = POINTS + 5 * %(runs)s, ALLTIME = ALLTIME + 5 * %(runs)s, POT_RATIO = ((POT_RATIO * (HALLS_LED - 1)) +"+str(r)+")/HALLS_LED WHERE UID = %(user)s"
            elif t == 1:
                sql = "UPDATE std_staff SET O3_LED = O3_LED + %(runs)s, POINTS = POINTS + 8 * %(runs)s, ALLTIME = ALLTIME + 8 * %(runs)s WHERE UID = %(user)s"
            elif t == 2:
                sql = "UPDATE std_staff SET EXALT_LED = EXALT_LED + %(runs)s, POINTS = POINTS + 3 * %(runs)s, ALLTIME = ALLTIME + 3 * %(runs)s WHERE UID = %(user)s"
            elif t == 3:
                sql = "UPDATE std_staff SET OTHER_LED = OTHER_LED + %(runs)s, POINTS = POINTS + 2 * %(runs)s, ALLTIME = ALLTIME + 2 * %(runs)s WHERE UID = %(user)s"
            else:
                sql = "UPDATE std_staff SET FAILED_RUNS = FAILED_RUNS + %(runs)s, POINTS = POINTS + %(runs)s, ALLTIME = ALLTIME + 1 * %(runs)s WHERE UID = %(user)s"
            cursor.execute(sql, {'user': uid,
                                'runs': r})
            connection.commit()
            cursor.close()
            print("Edited User %s %s %s" % (uid, t, r))
        else:
            print("Something went wrong")
            return "Failed to add User"
    except Error as e:
        print("Update User Fail", e)
        return "ERROR"


async def reset_all():
    try:
        if not connection is None:
            cursor = connection.cursor()
            sql = "UPDATE std_staff SET EXALT_LED = 0, O3_LED = 0, HALLS_LED = 0, OTHER_LED = 0, POINTS = 0, ALLTIME = 0, POT_RATIO = 0"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
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

async def fetch_staff(uid):
    if connection is None:
        await log("Please connect to the SQL server before attempting to make queries.", LogLevel.ERROR)
        return None
    try:
        cursor = connection.cursor(buffered=True)
        query = "SELECT DISTINCT * FROM std_staff WHERE uid = %(user)s"
        cursor.execute(query, {
            'user': uid
        })
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return None

        out: Dict = {
            'uid': data[0],
            'exalt': data[1],
            'o3': data[2],
            'halls': data[3],
            'other': data[4],
            'rolelevel': data[5],
            'points': data[6],
            'alltime': data[7],
            'potratio': data[8],
            'failed': data[9],
            'leave': data[10],
            'warn': data[11]
        }
        
        return out
    except Exception as e:
        await log("An error occurred when attempting to fetch user with UID " + str(uid) + ".", LogLevel.ERROR)
        connection.reconnect(attempts=3, delay=0)
        await log(e.__str__(), LogLevel.DEBUG)
        return None

async def addstaff(uid, level=0, pnts = 0):
    if connection is None:
        await log("Please connect to the SQL server before attempting to insert data.", LogLevel.ERROR)
        return False
    if await fetch_staff(uid) is not None:
        await log("User " + uid + " already exists in the database.", LogLevel.WARN)
        return False
    try:
        cursor = connection.cursor()
        query = "INSERT INTO std_staff VALUES (%(user)s, 0, 0, 0, 0, %(level)s, 0, %(points)s, 0, 0, false, 0)"
        cursor.execute(query, {'user': uid,
                               'level': level,
                               'points': pnts})
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        await log("An error occurred while adding a user.", LogLevel.ERROR)
        await log(e.__str__(), LogLevel.DEBUG)
        return False