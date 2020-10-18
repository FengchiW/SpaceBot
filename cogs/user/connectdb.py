import discord
from ..util import sql

def connectdb():
    sql.connect()
    return "connected"