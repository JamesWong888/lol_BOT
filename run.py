from discord.ext.commands import Bot
from discord import Game
import random
import asyncio
import requests
import time
import discord
import os
#import _staticData


APIKEY = 'RGAPI-dba999e3-52ec-4601-a2da-a06f3ea12dfc' # Riot Games
BOT_PREFIX = ('?', '!') # Bot will respond to messages which start with ? and !
REGION = 'euw1' 
client = commands.Bot(command_prefix = BOT_PREFIX)


@client.event # Displays the Eg. 'Playing League of Legends' message on discord.
async def on_ready():
    await client.change_presence(game=discord.Game(name =  ' with MeHead. ?help'))
    print('Logged in as ' + client.user.name)

async def list_servers(): # Displays all current servers the bot is running on.
    await client.wait_until_ready()
    print("Current servers: ")
    for server in client.servers:
        print(server.name)

def requestSummonerData(REGION, summonerName, APIKEY): # Returns JSON summoner info with input: Username
    URL = "https://" + REGION + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + APIKEY
    response = requests.get(URL) # Goes to URL and returns .json
    return response.json()

def requestRankedData(REGION, ID, APIKEY): # Returns RANKED with input: ID
    URL = "https://" + REGION + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + APIKEY
    response = requests.get(URL)
    return response.json()

def summonerNameToID(summonerName): # Username to ID
    responseJSON  = requestSummonerData(REGION, summonerName, APIKEY)
    try:
        return str(responseJSON['id'])
    except KeyError:
        return None

def nameToAccID(summonerName): # Finds ACCOUNT ID not ID
    responseJSON  = requestSummonerData(REGION, summonerName, APIKEY)
    try:
        return str(responseJSON['accountId'])
    except KeyError:
        return None
    
def findRealName(summonerName):
    responseJSON  = requestSummonerData(REGION, summonerName, APIKEY)
    try:
        return str(responseJSON['name'])
    except KeyError:
        return None

def requestRank(summonerName): # Returns a string/array with ONE user rank info in 'pretty format' with input: Username
    printQueue = {}
    ID = summonerNameToID(summonerName)
    if (ID == None):
        return None
    responseJSON2 = requestRankedData(REGION, ID, APIKEY)

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

def formatClock(seconds):
    mins = str(seconds // 60)
    seconds = str((seconds % 60)/100)
    try:
        seconds = seconds[2] + seconds[3]
    except IndexError:
        seconds = seconds[2] +  '0'
    return (mins + ":" + seconds)


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


@client.command(name = 'live', brief='Shows information about a live game.', pass_context = True)
async def activeGame(ctx, summonerName):

    printQueue = []
    mapName = ""
    responseJSON2 = requestSummonerData(REGION, summonerName, APIKEY)
    try:
        ID = str(responseJSON2['id'])
    except KeyError:
        await client.say(ctx.message.author.mention + ", '" + summonerName + "' not found. Please check spelling")
        return
    
    URL = "https://" + REGION + ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + APIKEY
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


@client.command(brief='Shows the free weekly champion rotation.')
async def rotation():
    URL = "https://" + REGION + ".api.riotgames.com/lol/platform/v3/champions?freeToPlay=true&api_key=" + APIKEY
    response = requests.get(URL)
    responseJSON = response.json()    
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
                     printQueue[9] + "```")



@client.command(brief='Shows the users last 5 matches.', pass_context=True)
async def history(ctx, summonerName):
    printQueue = []
    
    accID = nameToAccID(summonerName)
    if (accID == None):
        await client.say(ctx.message.author.mention + ", '" + summonerName + "' not found. Please check spelling")
        return
    name = findRealName(summonerName)
    URL = 'https://' + REGION + '.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(accID) + '?beginIndex=0&endIndex=5&api_key=' + APIKEY
    #URL = 'https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/220521642?beginIndex=0&endIndex=5&api_key=RGAPI-7f302503-2a1a-44b8-be02-2b853337fcc0'
    response = requests.get(URL)
    responseJSON = response.json()
    
    
    for counter in range(5):
        gameID = responseJSON['matches'][counter]['gameId']
        champID = responseJSON['matches'][counter]['champion']

        participantID = -1
        team = -1
        
        URL2 = 'https://' + REGION + '.api.riotgames.com/lol/match/v3/matches/' + str(gameID) + '?api_key=' + APIKEY
        response2 = requests.get(URL2)
        responseJSON2 = response2.json()
        
        
        time = responseJSON2['gameDuration'] # INT
        queueID = responseJSON2['queueId'] # INT
        mapName = _staticData.mapTypeDict[queueID] ## HOLDS THE QUEUE NAME EG. SUMMONERS RIFT 5V5 RANKED
        
        for participantCounter in range(10):
            if (responseJSON2['participantIdentities'][participantCounter]['player']['summonerName'] == name):  
                participantID = responseJSON2['participantIdentities'][participantCounter]['participantId']

        if participantID < 6:
            team = 0
        elif participantID > 5:
            team = 1

        win = responseJSON2['teams'][team]['win']
        if win == 'Win':
            win = 'VICTORY'
        elif win == 'Fail':
            win = 'DEFEAT'
        
        
        kills = str(responseJSON2['participants'][participantID-1]['stats']['kills'])
        deaths = str(responseJSON2['participants'][participantID-1]['stats']['deaths'])
        assists = str(responseJSON2['participants'][participantID-1]['stats']['assists'])
        kda = kills + "/" + deaths + "/" + assists

        
        
        goldEarned = str(responseJSON2['participants'][participantID-1]['stats']['goldEarned'])
        champName = _staticData.champDict["data"][str(champID)]['key']
        totalTime = formatClock(responseJSON2['gameDuration'])
        totalMinionsKilled = str(responseJSON2['participants'][participantID-1]['stats']['totalMinionsKilled'])


        printQueue.append('{:{widthChamp}} {:{widthKDA}} {:{widthGold}} {:{widthCS}}{:{widthTime}}{:{widthWin}}'
                          .format(champName,  kda, goldEarned, totalMinionsKilled, totalTime, win,
                                  widthChamp = 13, widthKDA = 9, widthGold = 6, widthCS = 5, widthTime = 8, widthWin = 5))


    printQueue.append('{:{widthChamp}} {:{widthKDA}} {:{widthGold}} {:{widthCS}}{:{widthTime}}{:{widthWin}}'
                          .format('Champion',  'Score', 'Gold', 'CS', 'Time', 'Result',
                                  widthChamp = 13, widthKDA = 9, widthGold = 6, widthCS = 5, widthTime = 8, widthWin = 5))
        
    await client.say("```Match History for: " + name + "\n\n" +
                     printQueue[5] + "\n" +
                     printQueue[0] + "\n" +
                     printQueue[1] + "\n" +
                     printQueue[2] + "\n" +
                     printQueue[3] + "\n" +
                     printQueue[4] + "```")



@client.command(brief='Shows an image of champion or rank.', pass_context=True)
async def image(ctx, name):
    #embed = discord.Embed(title="Servant Card", description="Current Card:", color=0x808080)
    #await client.say(embed=embed)
    
    try:
        await client.send_file(ctx.message.channel, name + 'Square.png')
    except FileNotFoundError:
        await client.say("Image not found. (" + name + ")")
'''
@client.command()
async def profile():
    #await client.say('Under Maintenance :)')
'''

##client.loop.create_task(list_servers()) # Lists the servers the bot is running on               
client.run(os.getenv('TOKEN'))
