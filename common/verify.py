import requests
import json
import codecs

# verify (ign, code) Verifies the user ouputing a code based on a player's realmeye statistics

# verify Str Str -> Str
def verify(ign, code):
    playerdata =  requests.get('https://nightfirec.at/realmeye-api/?player=' + (ign) + "&filter=desc1+desc2+desc3+player_last_seen+rank",
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})

    d = codecs.decode(playerdata.content)

    data = json.loads(d)
    try:
        line1 = data["desc1"]
    except Exception as e:
        print(e)
    try:
        line2 = data["desc2"]
    except Exception as e:
        print(e)
    try:
        line3 = data["desc3"]
    except Exception as e:
        print(e)

    try:
        stars = data["rank"]
    except Exception as e:
        print(e)  
    
    
    try:
        lochidden = data["player_last_seen"]
    except Exception as e:
        print(e)  

    if line1.find(code) > 0 or line2.find(code) > 0 or line3.find(code) > 0:
        if stars > 19:
            if lochidden == "hidden":
                return "SUCCESS"
            else:
                return "Location not hidden!"
        else:
            return "A minimum of 20 stars required you have %s" % (stars)
    else:
        return "No code detected; Your codes %s %s %s " % (line1, line2, line3)

def getlastchar(ign):
    pass
    #TODO : get the last char played's stats and equips