        uid = ctx.author.id
        if not name is None:
            uid = int(re.sub('[<!@>]', '', name))
        print(name, uid)
        
        user = await sql.fetch_staff(uid)

        if user is None:
            await sql.addstaff(uid, 1, 0)

        user = await sql.fetch_staff(uid)

        requiredpnts = 0

        if user['rolelevel'] == 1:
            requiredpnts = 40
        elif user['rolelevel'] == 0:
            requiredpnts = 0
        else:
            requiredpnts = 50

        embed=Embed    (title="Staff Stats",       description="<@!%s>" % (uid))
        embed.add_field(name="O3's led: ",         value="%s"   % (user['o3']),               inline=True)
        embed.add_field(name="Halls led: ",        value="%s"   % (user['halls']),            inline=True)
        embed.add_field(name="Exaltations Led: ",  value="%s"   % (user['exalt']),            inline=True)
        embed.add_field(name="Misc Led: ",         value="%s"   % (user['other']),            inline=True)
        embed.add_field(name="Weekly Points: ",    value="%s"   % (user['points']),           inline=True)
        embed.add_field(name="Required Points: ",  value="%s"   % requiredpnts,               inline=True)
        embed.add_field(name="All Time Points: ",  value="%s"   % (user['alltime']),          inline=True)
        embed.add_field(name="Pot Ratio: ",        value="%s"   % (user['potratio']),         inline=True)
        embed.add_field(name="Failed Runs: ",      value="%s"   % (user['failed']),           inline=True)
        embed.add_field(name="On Leave: ",         value="%s"   % (user['leave']),            inline=True)
        embed.add_field(name="Warnings: ",         value="%s"   % (user['warn']),             inline=True)
        await ctx.send(embed=embed)