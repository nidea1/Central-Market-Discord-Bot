import discord
import requests
import json
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Client log-in
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

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

                if k == "error":
                    return("Wait list is empty.")

                else:
                    if k == "name":
                        obj["Öğe"] = v

                    if k == "price":
                        obj["Fiyat"] = "{:,d}".format(v)

                    if k == "liveAt":
                        date = datetime.fromtimestamp(v).strftime("%H:%M:%S")
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
                    return("Wait list is empty.")

            else:
                if k == "name":
                    obj["Öğe"] = v

                if k == "price":
                    obj["Fiyat"] = str("{:,d}".format(v))

                if k == "liveAt":
                    date = datetime.fromtimestamp(v).strftime("%H:%M:%S")
                    obj["Listeleneceği saat"] = str(date)

        # this loop our values converting to string
        for key,val in obj.items():
            converted += key + " : " + val + "\n"
        return(converted)
        


# BOT EVENTS
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.!waitlist'):
        waitlist = WaitList()
        await message.channel.send("```" +waitlist+"```")
      
    if message.content.startswith('.!help'):
        await message.channel.send("```.!waitlist : Merkez pazara yeni kaydedilen öğelerin satışta olacağı saat verilerini getirir.```")
        

client.run('TOKEN')