import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os
import random
import requests
import ast
import json

import _staticData 

Client = discord.Client()
client = commands.Bot(command_prefix = '?')
REGION = os.getenv('REGION')
RIOTKEY = os.getenv('RIOTKEY')


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name =  ' now running 24/7!'))
    print('Logged in as ' + client.user.name)

    
@client.command()
async def testy():
    await client.say("hello")  

def formatClock(seconds):
    mins = str(seconds // 60)
    seconds = str((seconds % 60)/100)
    try:
        seconds = seconds[2] + seconds[3]
    except IndexError:
        seconds = seconds[2] +  '0'
    return (mins + ":" + seconds)
    
def findRealName(summonerName):
    responseJSON  = requestSummonerData(REGION, summonerName, RIOTKEY)
    try:
        return str(responseJSON['name'])
    except KeyError:
        return None    
    
def requestSummonerData(REGION, summonerName, RIOTKEY): # Returns JSON summoner info with input: Username
    URL = "https://" + REGION + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + RIOTKEY
    response = requests.get(URL) # Goes to URL and returns .json
    return json.loads(response.text)

def requestRankedData(REGION, ID, RIOTKEY): # Returns RANKED with input: ID
    URL = "https://" + REGION + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + RIOTKEY
    response = requests.get(URL)
    return json.loads(response.text)
    
def summonerNameToID(summonerName): # Username to ID
    responseJSON = requestSummonerData(REGION, summonerName, RIOTKEY)

    try:
        return str(responseJSON['id'])
    except KeyError:
        return None
    
def nameToAccID(summonerName): # Finds ACCOUNT ID not ID
    responseJSON  = requestSummonerData(REGION, summonerName, RIOTKEY)
    try:
        return str(responseJSON['accountId'])
    except KeyError:
        return None
    

def requestRank(summonerName): # Returns a string/array with ONE user rank info in 'pretty format' with input: Username
    printQueue = {}
    ID = summonerNameToID(summonerName)
    if (ID == None):
        return None
    responseJSON2 = requestRankedData(REGION, ID, RIOTKEY)
    
    num = 3
    for i in range(1):
        try:
            if (responseJSON2[0]["queueType"] == "RANKED_SOLO_5x5"):
                num = 0
            elif (responseJSON2[1]["queueType"] == "RANKED_SOLO_5x5"):
                num = 1
        except Exception:
            continue
        
        finally:
            if (num == 0 or num == 1):
                summonerName = str(responseJSON2[num]['playerOrTeamName'])
                rank = str.title(responseJSON2[num]['tier']) + " " + str(responseJSON2[num]['rank'])
                winRate = str(responseJSON2[num]['wins']*100//(responseJSON2[num]['losses']+responseJSON2[num]['wins'])) + "%"
                gamesPlayed = str(responseJSON2[num]['wins'] + responseJSON2[num]['losses']) + "G"
                
                printQueue['summonerName'] = summonerName
                printQueue['rank'] = rank
                printQueue['winRate'] = winRate
                printQueue['gamesPlayed'] = gamesPlayed

            elif (num == 3):
                printQueue['summonerName'] = str(summonerName)
                printQueue['rank'] = 'Unranked'
                printQueue['winRate'] = "N/A"
                printQueue['gamesPlayed'] = "N/A"
                
            else:
                printQueue.append(str("Error Summoner: " + summonerName))        

    return printQueue


@client.command(brief = 'Shows the users solo queue rank.', pass_context = True)
async def rank(ctx, summonerName):

    summonerInfo = requestRank(summonerName)
    if (summonerInfo == None):
        await client.say(ctx.message.author.mention + ", '" + summonerName + "' not found. Please check spelling")
        return
    
    await client.say ("```" + summonerInfo['summonerName'] + "  " +
                      summonerInfo['rank'] + "  " +
                      summonerInfo['winRate'] + "  " +
                      summonerInfo['gamesPlayed'] + "```")


@client.command(brief='Shows the free weekly champion rotation.')
async def rotation():
    URL = "https://" + REGION + ".api.riotgames.com/lol/platform/v3/champions?freeToPlay=true&api_key=" + RIOTKEY
    response = requests.get(URL)
    responseJSON = json.loads(response.text)  
    printQueue = []
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
                     printQueue[9] + "\n" +
                     printQueue[10] + "\n" +
                     printQueue[11] + "\n" +
                     printQueue[12] + "\n" +
                     printQueue[13] + "```")

 

@client.command(name = 'live', brief='Shows information about a live game.', pass_context = True)
async def activeGame(ctx, summonerName):

    printQueue = []
    mapName = ""
    responseJSON2 = requestSummonerData(REGION, summonerName, RIOTKEY)
    try:
        ID = str(responseJSON2['id'])
    except KeyError:
        await client.say(ctx.message.author.mention + ", '" + summonerName + "' not found. Please check spelling")
        return
    
    URL = "https://" + REGION + ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + RIOTKEY
    response = requests.get(URL)
    responseJSON = response.json()

    mapID = -1 # There is no map with -1
    try:
        mapID = responseJSON['gameQueueConfigId']
    except Exception:
        await client.say(responseJSON2['name'] + " is not in a game") ## current
        return
    mapName = _staticData.mapTypeDict[mapID]
    clock = formatClock(responseJSON['gameLength'])

    maxChampLen = 0
    maxNameLen = 0
    maxRankLen = 0
        
    for counter in range(10):
        summonerName = responseJSON['participants'][counter]['summonerName']  
        champID = responseJSON['participants'][counter]['championId']
        champName = _staticData.champDict["data"][str(champID)]['key']
       
        summonerInfo = requestRank(summonerName)
        if len(champName) > maxChampLen:
              maxChampLen = len(champName)
        if len(summonerInfo['summonerName']) > maxNameLen:
            maxNameLen = len(summonerInfo['summonerName'])
        if len(summonerInfo['rank']) > maxRankLen:
              maxRankLen = len(summonerInfo['rank'])


    for counter in range(10):
        summonerName = responseJSON['participants'][counter]['summonerName']  
        champID = responseJSON['participants'][counter]['championId']
        champName = _staticData.champDict["data"][str(champID)]['key']
       
        summonerInfo = requestRank(summonerName)
        #await client.say(summonerName)
        printQueue.append('{:{widthChamp}} {:{widthName}} {:{widthRank}} {:{widthWin}}{:{widthGames}}'
                          .format(champName,  summonerInfo['summonerName'], summonerInfo['rank'], summonerInfo['winRate'], summonerInfo['gamesPlayed'],
                                  widthChamp = maxChampLen+1, widthName = maxNameLen+1, widthRank = maxRankLen+1, widthWin = 5, widthGames = 5))


    await client.say("```" + mapName + " | " + clock +
                     "\n\n----------- TEAM 1 ------------------------------\n" +
                     printQueue[0] + "\n" +
                     printQueue[1] + "\n" +
                     printQueue[2] + "\n" +
                     printQueue[3] + "\n" +
                     printQueue[4] +
                     "\n\n----------- TEAM 2 ------------------------------\n" +
                     printQueue[5] + "\n" +
                     printQueue[6] + "\n" +
                     printQueue[7] + "\n" +
                     printQueue[8] + "\n" +
                     printQueue[9] + "```")


    
client.run(os.getenv('BOTTOKEN'))

