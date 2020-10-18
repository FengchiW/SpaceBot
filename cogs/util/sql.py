import random
import mysql.connector
from mysql.connector import Error

connection = None

def connect():
    global connection
    connection = None
    try:
        connection = mysql.connector.connect(
            host = 'li2140-92.members.linode.com',
            port = 3306,
            database = 'STD',
            user = 'sqladmin',
            password = 'sqladmin'
        )
    except Error as e:
        print("Something went wrong connecting to Server", e)

    print("connection success")
    return True

def add_user(ign, gid, uid):
    if fetch_user(gid, uid) is None:
        code = "STD"+str(random.randint(100,999))
        try:
            if not connection is None:
                cursor = connection.cursor()
                sql = "INSERT INTO `%(guild)s` VALUES (%(user)s, %(code)s, %(ign)s, 'NONE', 0, 0, 0, 0, 0, 'NONE', 0)"
                cursor.execute(sql, {'guild': gid,
                                     'user' : uid,
                                     'code' : code,
                                     'ign'  : ign})
                connection.commit()
                cursor.close()
                return "Added User"
            else:
                print("Something went wrong")

                return "Failed to add User"
        except Error as e:
            print(e)
            return "ERROR"

def fetch_user(gid, uid):
    try:
        if not connection is None:
            cursor = connection.cursor(buffered=True)
            sql = "SELECT * FROM `%(guild)s` WHERE ID = %(user)s"
            cursor.execute(sql, {'guild': gid,
                                 'user' : uid})

            data = cursor.fetchone()

            if data is None:
                return None
            
            out = {
                "UID"   : data[0],
                "CODE"  : data[1],
                "IGN"   : data[2],
                "ALT"   : data[3],
                "O3"    : data[4],
                "RUNS"  : data[5],
                "KEYS"  : data[6],
                "RUNES" : data[7],
                "VIALS" : data[8],
                "ROLES" : data[9],
                "POINTS": data[10],
            }

            return out
        else:
            print("Fetch User Fail: Connection not established, reconnecting")
            connect()
            return None
    except Error as e:
        connect()
        print("Fetch User Fail: ", e)
        return None

def fetch_leaderboard(gid):
    try:
        if not connection is None:
            cursor = connection.cursor(buffered=True)
            sql = "SELECT * FROM `%(guild)s` ORDER BY KEY_POPS DESC limit 10"
            cursor.execute(sql, {'guild': gid})

            data = cursor.fetchall()

            print("Result: ", data)

            return data
        else:
            print("Something went wrong")
            return None
    except Error as e:
        connect()
        print("Fetch User Fail: ", e)
        return None

def update_user(uid, column, change, gid):
    try:
        if fetch_user(gid, uid) is None:
            add_user("Null", gid, uid)
        if not connection is None:
            cursor = connection.cursor()
            sql = "UPDATE `%(guild)s` SET `%(col)s` = `%(value)s` WHERE id = `%(user)s`"
            cursor.execute(sql, {'guild': gid,
                                 'col'  : column,
                                 'value': change,
                                 'user' : uid})
            connection.commit()
            return "Edited User %s %s %s" % (column, change, uid)
        else:
            print("Something went wrong")

            return "Failed to add User"
    except Error as e:
        print("Update User Fail", e)
        return "ERROR"

def logkey(uid, keys, gid):
    newkeys = fetch_user(gid, uid)[6] + keys
    update_user(uid, 'KEY_POPS', newkeys, gid)

def logvile(uid, viles, gid):
    newviles = fetch_user(gid, uid)[8] + viles
    update_user(uid, 'VILES', newviles, gid)

def logrune(uid, runes, gid):
    newrunes = fetch_user(gid, uid)[7] + runes
    update_user(uid, 'RUNES', newrunes, gid)

def changeName(uid, name, gid):
    newnick = "\""+name+"\""
    update_user(uid, 'IGN', newnick, gid)