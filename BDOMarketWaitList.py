import discord
from discord.ext import tasks
import requests
import json
from datetime import datetime
import pytz


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

new_timezone = pytz.timezone("Europe/Istanbul")

# Client log-in
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

def Lunar():
    # Use the json module to load the string data into a dictionary
    response = requests.get("https://api.arsha.io/v2/mena/orders?id=11663&sid=5")
    theJSON = json.loads(response.text)
    # Created a new dict for our getted datas
    obj = {"Fiyat": "", "Satış": "", "Sipariş": ""}
    # converted variable for our messages
    converted = str()
    nonline = "\n" + "------------------------------------ \n \n"

    # now we can access the contents of the JSON like any other Python object
    for k,v in theJSON.items():
        if type(theJSON[k]) == list:
            for i in range(len(theJSON[k])):   
                for key,val in theJSON[k][i].items():

                    if key == "price":
                        obj["Fiyat"] = str("{:,d}".format(val))

                    if key == "buyers":
                        obj["Satış"] = val

                    if key == "sellers":
                        obj["Sipariş"] = val

                # this loop our values converting to string
                for key,val in obj.items():
                    converted += key + " : " + str(val) + "\n" 
                converted += nonline
            return(converted)

def Disto():
    # Use the json module to load the string data into a dictionary
    response = requests.get("https://api.arsha.io/v2/mena/orders?id=11853&sid=5")
    theJSON = json.loads(response.text)
    # Created a new dict for our getted datas
    obj = {"Fiyat": "", "Satış": "", "Sipariş": ""}
    # converted variable for our messages
    converted = str()
    nonline = "\n" + "------------------------------------ \n \n"

    # now we can access the contents of the JSON like any other Python object
    for k,v in theJSON.items():
        if type(theJSON[k]) == list:
            for i in range(len(theJSON[k])):             
                for key,val in theJSON[k][i].items():

                    if key == "price":
                        obj["Fiyat"] = str("{:,d}".format(val))

                    if key == "buyers":
                        obj["Satış"] = val

                    if key == "sellers":
                        obj["Sipariş"] = val

                # this loop our values converting to string
                for key,val in obj.items():
                    converted += key + " : " + str(val) + "\n" 
                converted += nonline
            return(converted)


# BDO-MENA Market
def WaitList():
    # Use the json module to load the string data into a dictionary
    response = requests.get("https://api.arsha.io/v2/mena/GetWorldMarketWaitList?lang=tr")
    theJSON = json.loads(response.text)
    # Created a new dict for our getted datas
    obj = {"Öğe": "", "Fiyat": "", "Listeleneceği saat": ""}
    # converted variable for our messages
    converted = str()
    nonline = "\n" + "------------------------------------" + "\n" + "\n"

    # We querying if it's a list. Cuz theJSON has can more data
    if type(theJSON) == list:

        # i converting list to dict
        for i in range(len(theJSON)):

            # now we can access the contents of the JSON like any other Python object
            for k,v in theJSON[i].items():
              
                if k == "name":
                    obj["Öğe"] = v

                if k == "price":
                    obj["Fiyat"] = "{:,d}".format(v)

                if k == "liveAt":
                    date = datetime.fromtimestamp(v).astimezone(new_timezone).strftime("%H:%M:%S")
                    obj["Listeleneceği saat"] = date

            # this loop our values converting to string
            for key,val in obj.items():
                converted += key + " : " + str(val) + "\n"
            converted += nonline
        return(converted)
        
                    

    # if theJSON is not list, it has 1 data and it's dict
    else:

        # now we can access the contents of the JSON like any other Python object
        for k,v in theJSON.items():

            if k == "error":
                    return("Şu anda pazar kaydını bekleyen öğe yok.")

            else:
                if k == "name":
                    obj["Öğe"] = v

                if k == "price":
                    obj["Fiyat"] = str("{:,d}".format(v))

                if k == "liveAt":
                    date = datetime.fromtimestamp(v).astimezone(new_timezone).strftime("%H:%M:%S")
                    obj["Listeleneceği saat"] = str(date)

        # this loop our values converting to string
        for key,val in obj.items():
            converted += key + " : " + val + "\n"
        return(converted)
        
# Spamming waitlist loop
@tasks.loop(seconds= 15)
async def WaitListLoop(ctx):
    waitlist = WaitList()
    channel = ctx.channel.name
    restricted_channels = ["apptest"]
    if channel in restricted_channels:
        await ctx.channel.send("```" +waitlist+"```", delete_after=15)

# BOT EVENTS
@client.event
async def on_message(ctx):
    nonline = "\n" + "------------------------------------ \n \n"

    # for a specific channel
    channel = ctx.channel.name
    restricted_channels = ["apptest"]
    if channel in restricted_channels:

        if ctx.author == client.user:
            return

        if ctx.content == "-list loop":
            WaitListLoop.start(ctx)
        
        if ctx.content == "-list":
            await ctx.channel.send("""```-list loop:\n  "Pazar Kaydı" döngüsünü başlatır.\n\n-list pen uyanan:\n  "PEN: Uyanan Ay Kolyesi" bilgilerini listeler.\n\n-list pen çöküş:\n  "PEN: Kara Çöküş Küpesi" bilgilerini listeler.```""")

        if ctx.content == "-list pen uyanan":
            lunar = Lunar()
            await ctx.channel.send("```PEN: Uyanan Ay Kolyesi" + nonline + lunar+"```")

        if ctx.content == "-list pen çöküş":
            disto = Disto()
            await ctx.channel.send("```PEN: Kara Çöküş Küpesi" + nonline + disto+"```")

        

client.run('TOKEN')