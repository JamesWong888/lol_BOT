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
    await client.change_presence(game=discord.Game(name =  ' running 24/7! test5'))
    print('Logged in as ' + client.user.name)

@client.command()
async def testy():
    await client.say("hello")

@client.command(brief='Shows the free weekly champion rotation.')
async def rotation():
    URL = "https://" + REGION + ".api.riotgames.com/lol/platform/v3/champions?freeToPlay=true&api_key=" + APIKEY
    response = requests.get(URL)
    responseJSON = response.json()    
    printQueue = []
    
    await client.("Success!")
    
    for counter in range(14):
        champID = responseJSON['champions'][counter]['id']
        champName = _staticData.champDict['data'][str(champID)]['key']
        champTitle = _staticData.champDict['data'][str(champID)]['title'] # Eg. Lux:   The Lady of Luminosity
        printQueue.append('{:15}{:10}'.format(champName, champTitle))

    await client.say("```This week's free rotation is: \n\n" +
                     printQueue[0] + "\n" +
                     printQueue[1] + "\n" +
                     printQueue[2] + "\n" +
                     printQueue[3] + "\n" +
                     printQueue[4] + "\n" +
                     printQueue[5] + "\n" +
                     printQueue[6] + "\n" +
                     printQueue[7] + "\n" +
                     printQueue[8] + "\n" +
                     printQueue[9] + "```")




client.run(os.getenv('TOKEN'))

