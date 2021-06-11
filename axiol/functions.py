from variables import DEFAULT_PREFIX, E_ERROR
from database import PREFIXES, LEVELDATABASE, PLUGINS

def getprefix(ctx):
    try:
        return PREFIXES.find_one({"_id": ctx.guild.id}).get("prefix")
    except AttributeError:
        return DEFAULT_PREFIX
    

def getxprange(message):
    col = LEVELDATABASE.get_collection(str(message.guild.id))
    settings = col.find_one({"_id": 0})
    xprange =settings.get("xprange")
    return xprange


async def pagination(ctx, current_page, embed, GuildCol, all_pages):
    pagern = current_page + 1
    embed.set_footer(text=f"Page {pagern}/{all_pages}")
    embed.clear_fields()

    rankings = GuildCol.find({

            "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
            
        }).sort("xp", -1)

    rankcount = (current_page)*10
    user_amount = current_page*10
    for i in rankings[user_amount:]:
        rankcount += 1
        getuser = ctx.guild.get_member(i.get("_id"))
        xp = i.get("xp")
        if getuser == None:
            user = f"{E_ERROR} This user has left the server"
        else:
            user = getuser
        embed.add_field(name=f"{rankcount}: {user}", value=f"Total XP: {xp}", inline=False)
        if rankcount == (current_page)*10 + 10:
            break



#Some functions to counter errors and warning while working locally :p

#Adding new plugin
def updateplugins(plugin):
    PLUGINS.update_many(
        { plugin: { "$exists": False } },
            {
                "$set": { plugin : False }
            }
    )

#updating leveling and plugin data
def updatedb(serverid):

    if not str(serverid) in LEVELDATABASE.list_collection_names():
        GuildLevelDB = LEVELDATABASE.create_collection(str(serverid))
        GuildLevelDB.insert_one({

            "_id": 0,
            "xprange": [15, 25],
            "alertchannel": None,
            "blacklistedchannels": [],
            "alerts": True
            }) 
        print(f"Added Leveling {serverid}")

    if not PLUGINS.count_documents({"_id": serverid}, limit=1):
        PLUGINS.insert_one({

                    "_id":serverid,
                    "Leveling":True,
                    "Moderation": True,
                    "Reaction Roles": True,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": False,
                    "Music": True
                })
        print(f"Added Plugins {serverid}")

    try:
        PREFIXES.insert_one({
            "_id": serverid,
            "prefix": "ax"
        })
        print(f"Added prefix {serverid}")

    except:
        print(f"Already there {serverid}")


serveridlist = []
#for i in serveridlist:
    #updatedb(i)
#updateplugins()
