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
    await client.change_presence(game=discord.Game(name =  ' running 24/7!'))
    print('Logged in as ' + client.user.name)

    
@client.command()
async def rotation():
        
    await client.say("Success!1")
    URL = "https://euw1.api.riotgames.com/lol/platform/v3/champions?freeToPlay=true&api_key=RGAPI-cece9a7b-953a-4d6c-89b9-6e8609135e91"

    response = requests.get(URL)

    responseTEXT = response.text
   
    printQueue = []

    
    for counter in range(14):
        champID = responseTEXT['champions'][counter]['id']
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


    
@client.command()
async def testy():
    await client.say("hello")

@client.command()
async def requestSummonerData(summonerName): # Returns JSON summoner info with input: Username
    URL = "https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=RGAPI-cece9a7b-953a-4d6c-89b9-6e8609135e91"
    await client.say("1")
    response = requests.get(URL) # Goes to URL and returns .json
    await client.say(response)
    JSON = response.json()
    await client.say("3")

    a = JSON['id']
    await client.say("4")
    await client.say(a)


client.run(os.getenv('TOKEN'))

