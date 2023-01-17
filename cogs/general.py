import os
import sys
import json
import requests
import itertools
from datetime import datetime

import discord
from discord import Colour
from discord.ext import commands, tasks
from discord.ext.commands import Context


class General(commands.Cog, name="general"):

    def __init__(self, bot):
        self.bot = bot
        #DATA
        if os.path.exists("data.json"):
            self.data = json.load(open("data.json"))
        else:
            sys.exit("data.json not found! Please add it and try again.")

        #STATICS
        self.region_id = "region_id"
        self.item_id = "item_id"
        self.sid = "sid"
        self.grade = "grade"
        self.item_name = "item_name"
        self.BTitle = "Merkez Pazar"
        self.nonline = "\n" + "\n" + "------------------------------------" + "\n" + "\n" 
        self.language = "tr"
        self.server = "mena"
        self.ITitle = self.grade + " " + self.item_name

    def run(self):

        #DYNAMICS
        link = f"https://api.arsha.io/v2/{self.server}/orders?id={self.item_id}&sid={self.sid}&lang={self.language}"
        response = requests.get(link)
        self.theJSON = json.loads(response.text)
        self.ITitle = self.grade + " " + self.item_name

    def waitlistrun(self):
        link = f"https://api.arsha.io/v2/{self.server}/GetWorldMarketWaitList?lang={self.language}"
        response = requests.get(link)
        self.theJSON = json.loads(response.text)

    @commands.hybrid_command(
        name="help",
        description="List of the available commands:"
    )
    async def help(self, context: Context) -> None:
        prefix = "-"
        embed = discord.Embed(
            title="Help",
            description="List of the available commands:",
            color=Colour.blue())
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            comdata= []
            for command in commands:
                desc = command.description.partition('\n')[0]
                comdata.append(f"{prefix}{command.name} - {desc}")
            text = "\n".join(comdata)
            embed.add_field(
            name=i.capitalize(),
            value=f"""```fix\n{text}```""",
            inline=False)
        await context.send(embed=embed)
    
    @commands.hybrid_command(
        name="lang",
        description="Central market language setting."
    )
    async def lang(self, context: Context, arg1 = "tr") -> None:
        arg1 = arg1.lower()

        if arg1 in self.data["languages"]:
            self.language = arg1
            embed = discord.Embed(
                title=self.BTitle,
                description="-lang :lang",
                color=0x9C84EF)
            embed.add_field(
                name="Central Market Language",
                value=f"""```arm\nCentral market language is {self.language.upper()} now.```""",
                inline=False)
        else:
            embed = discord.Embed(
                title=self.BTitle,
                description="-lang :lang",
                color=0x9C84EF)
            embed.add_field(
                name="Central Market Language",
                value=f"""```arm\nYou did enter a wrong language.```""",
                inline=False)

        await context.send(embed=embed)

    @commands.hybrid_command(
    name="region",
    description="Central market region setting."
    )
    async def region(self, context: Context, arg1 = "mena") -> None:
        arg1 = arg1.lower()

        if arg1 in self.data["regions"]:
            self.server = arg1
            embed = discord.Embed(
                title=self.BTitle,
                description="""```fix\n-region :region```""",
                color=0x9C84EF)
            embed.add_field(
                name="Central Market Region",
                value=f"""```fix\nCentral market region is {self.server.upper()} now.```""",
                inline=False)
        else:
            embed = discord.Embed(
                title=self.BTitle,
                description="""```fix\n-region :region```""",
                color=0x9C84EF)
            embed.add_field(
                name="Central Market Region",
                value=f"""```fix\nYou did enter a wrong region.```""",
                inline=False)

        await context.send(embed=embed)



    @commands.hybrid_command(
    name="list",
    description="Central Market item list.",
    )
    async def list(self, context: Context, arg1="", arg2="0") -> None:
        arg1 = arg1.lower()
        arg2 = arg2.lower()
        
        #ITEMS
        for i in self.data["items"]:
            if arg1 in i["search"]:
                self.item_id = i["id"]
                self.item_name = str(i["name"])
                Ltxt = "Listing..."
                break

            elif arg1 == "help":
                embed = discord.Embed(
                    title=self.BTitle,
                    description="""```fix\n-list :items :grades :regions```""",
                    color=Colour.blue())
                for i in dict(itertools.islice(self.data.items(), 4)):
                    commands= []
                    for x in self.data[i]:
                        if type(x) == dict:
                            commands.append(x["name"])
                        else:
                            commands.append(x)
                    embed.add_field(
                    name=i,
                    value=f"""```fix\n{", ".join(map(str,commands))}```""",
                    inline=False)

            elif arg1 == "":
                embed = discord.Embed(
                    title=self.BTitle,
                    description="""```fix\n-list :items :grades :regions```""",
                    color=0x9C84EF)
                embed.add_field(
                    name=self.ITitle,
                    value=f"""```fix\nYou did not enter a item.```""",
                    inline=False)
            else:
                Ltxt = self.data["errors"][self.language][0]
                self.item_name = str()

        #GRADES
        for k,v in self.data["grades"].items():
            if arg2 in v:
                self.grade = str(v[0]).upper()+":"
                self.sid = k
                Ltxt = "Listing..."
                if arg2 == "0":
                    self.grade = str(v[0]).upper()
                    self.sid = k
                    Ltxt = "Listing..."
                    break
                else:
                    break
            else:
                Ltxt = self.data["errors"][self.language][1]
                self.grade = ""

        #RUN
        if Ltxt in self.data["errors"][self.language] or arg1 == "":
            pass
        else:
            self.run()
            Ltxt = str()
            Lsort = dict()
            for i in range(len(self.theJSON["orders"])):
                Lsort[i] = self.theJSON["orders"][i]

            res = sorted(Lsort.items(), key = lambda x: x[1]['price'])
            res.reverse()
            res = dict(res)

            embed = discord.Embed(
                    title=self.BTitle,
                    description=f"""```arm\nServer: {self.server.upper()}```""",
                    color=0x9C84EF)
            for x in res:
                Ltxt = "Price: " + "{:,d}".format(res[x]["price"]) + "\n" + "Sellers: " + "{:,d}".format(res[x]["buyers"]) + "\n" + "Buyers: " + "{:,d}".format(res[x]["sellers"])
                embed.add_field(
                    name=self.ITitle if x == list(res)[0] else "",
                    value=f"""```arm\n{Ltxt}```""",
                    inline=False)


                    

        await context.send(embed=embed)

    @commands.hybrid_command(
        name="waitlist",
        description = "Central Market in registration queue list."
    )
    async def waitlist(self, context: Context):
        self.waitlistrun()
        WLtxt = str()
        embed = discord.Embed(
            title=self.BTitle,
            description=f"""```arm\nServer: {self.server.upper()}```""",
            color=0x9C84EF)

        if type(self.theJSON) == list:
            for i in range(len(self.theJSON)):
                WLtxt = "Price: " + "{:,d}".format(self.theJSON[i]["price"]) + "\n" + "LiveAt: " + datetime.fromtimestamp(self.theJSON[i]["liveAt"]).strftime("%H:%M:%S")
                embed.add_field(
                    name=self.theJSON[i]["name"].replace("&#39;","'"),
                    value=f"""```arm\n{WLtxt}```""",
                    inline=False)
        else:
            if list(self.theJSON)[0] == "error":
                WLtxt = "There are no items in registration queue."
                embed.add_field(
                    name="In registration queue",
                    value=f"""```arm\n{WLtxt}```""",
                    inline=False)
            else:
                WLtxt = "Price: " + "{:,d}".format(self.theJSON["price"]) + "\n" + "LiveAt: " + datetime.fromtimestamp(self.theJSON["liveAt"]).strftime("%H:%M:%S")
                embed.add_field(
                    name=self.theJSON["name"].replace("&#39;","'"),
                    value=f"""```arm\n{WLtxt}```""",
                    inline=False)
        
        

        await context.send(embed=embed, delete_after=15)

    @commands.hybrid_command(
        name="loop",
        description = "Central Market in registration queue loop."
    )
    async def loop(self, context: Context, arg1=""):
        arg1 = arg1.lower()

        embed = discord.Embed(
                title=self.BTitle,
                description="""```fix\n-loop help | start | stop region```""",
                color=0x9C84EF)

        if arg1 == "":
            embed.add_field(
                name="In registration queue",
                value=f"""```fix\nYou did not enter a command.```""",
                inline=False)
            await context.send(embed=embed)

        elif arg1 == "help":
            embed.add_field(
                name="In registration queue",
                value=f"""```fix\nThis loop is replacing every 15 seconds.```""",
                inline=False)
            await context.send(embed=embed)        

        elif arg1 == "start":
            self.WaitListLoop.start(context)

        elif arg1 == "stop":
            self.WaitListLoop.cancel()

        else:
            embed.add_field(
                name="In registration queue",
                value=f"""```fix\nYou did enter a wrong command.```""",
                inline=False)
            await context.send(embed=embed)
        

        


    @tasks.loop(seconds= 15)
    async def WaitListLoop(self, context : Context):
        await self.waitlist(context)





async def setup(bot):
    await bot.add_cog(General(bot))