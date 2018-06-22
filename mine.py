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
REGION = 'euw1'
APIKEY = 'RGAPI-cece9a7b-953a-4d6c-89b9-6e8609135e91'

@client.event # Displays the Eg. 'Playing League of Legends' message on discord.
async def on_ready():
    await client.change_presence(game=discord.Game(name =  ' running 24/7! test7'))
    print('Logged in as ' + client.user.name)

    
@client.command()
async def rotation():
        
    await client.say("Success!1")
    URL = "https://" + REGION + ".api.riotgames.com/lol/platform/v3/champions?freeToPlay=true&api_key=" + APIKEY
        
    await client.say("Success!2")
    response = requests.get(URL)
        
    await client.say("Success!3")
    await client.say(response)
    responseJSON = response.json()
        
    await client.say("Success!4")
    printQueue = []
    
    await client.say("Success!5")
    

    
@client.command()
async def testy():
    await client.say("hello")




client.run(os.getenv('TOKEN'))

