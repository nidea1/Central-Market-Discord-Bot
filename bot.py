import os
import random
import platform
import asyncio


import discord
from discord import Colour
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

load_dotenv()


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


bot = Bot(command_prefix = "-", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print(f"Python version: {platform.python_version()}")
    print(f"discord.py API version: {discord.__version__}")
    print("-------------------")
    status_task.start()

@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", "with Discord!", "with humans!", "with Central Market!", "with Black Desert Online!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@bot.event
async def on_message(message: discord.Message):
    channel = message.channel.name
    restricted_channels = ["central-market"]
    if channel in restricted_channels:
        if message.author == bot.user or message.author.bot:
            return
        await bot.process_commands(message)

@bot.event
async def on_command_error(context: Context, error):

    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color= Colour.brand_red()
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color= Colour.brand_red()
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="I am missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to fully perform this command!",
            color= Colour.brand_red()
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color= Colour.brand_red()
        )
        await context.send(embed=embed)
    else:
        raise error

async def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

asyncio.run(load_cogs())
bot.run(os.getenv("TOKEN"))