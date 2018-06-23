import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os
import random
import requests

Client = discord.Client()
client = commands.Bot(command_prefix = '?')
REGION = os.getenv('REGION')
RIOTKEY = os.getenv('RIOTKEY')


@client.event # Displays the Eg. 'Playing League of Legends' message on discord.
async def on_ready():
    await client.change_presence(game=discord.Game(name =  ' now running 24/7!'))
    print('Logged in as ' + client.user.name)

@client.command()
async def testy():
    await client.say("hello")
    await client.say(REGION)
    await client.say(RIOTKEY)

client.run(os.getenv('BOTTOKEN'))

