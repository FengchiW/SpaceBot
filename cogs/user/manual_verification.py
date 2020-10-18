import discord
from ..util import sql

def manver(ign, uid, gid):
    data = sql.add_user(ign, gid, uid)