import sqlite3
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

def add_user(ign, uid):
    if fetch_user(uid) is None:
        code = "STD"+str(random.randint(100,999))
        try:
            if not connection is None:
                cursor = connection.cursor()
                sql = "INSERT INTO STD VALUES (%s, %s, %s, 'NONE', 0, 0, 0, 0, 0, 'NONE')"
                values = (uid, code, ign)
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                return "Added User %s %s %s" % values
            else:
                print("Something went wrong")

                return "Failed to add User"
        except Error as e:
            print(e)
            return "ERROR"

def fetch_user(uid):
    try:
        if not connection is None:
            cursor = connection.cursor(buffered=True)
            sql = "SELECT * FROM STD WHERE ID = %s" % (uid)
            cursor.execute(sql)

            data = cursor.fetchone()

            print("Result: ", data)

            return data
        else:
            print("Something went wrong")
            return None
    except Error as e:
        connect()
        print("Fetch User Fail: ", e)
        return None

def fetch_leaderboard():
    try:
        if not connection is None:
            cursor = connection.cursor(buffered=True)
            sql = "SELECT * FROM STD ORDER BY KEY_POPS DESC limit 10"
            cursor.execute(sql)

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

def update_user(uid, column, change):
    try:
        if fetch_user(uid) is None:
            add_user("Null", uid)
        if not connection is None:
            cursor = connection.cursor()
            sql = "UPDATE STD SET %s = %s WHERE id = %s" % (column, change, uid)
            cursor.execute(sql)
            connection.commit()
            return "Edited User %s %s %s" % (column, change, uid)
        else:
            print("Something went wrong")

            return "Failed to add User"
    except Error as e:
        print("Update User Fail", e)
        return "ERROR"

def logkey(uid, keys):
    newkeys = fetch_user(uid)[6] + keys
    update_user(uid, 'KEY_POPS', newkeys)

def logvile(uid, viles):
    newviles = fetch_user(uid)[8] + viles
    update_user(uid, 'VILES', newviles)

def logrune(uid, runes):
    newrunes = fetch_user(uid)[7] + runes
    update_user(uid, 'RUNES', newrunes)

def changeName(uid, name):
    newnick = "\""+name+"\""
    update_user(uid, 'IGN', newnick)