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
#client.remove_command('help')

APIKEY = 'RGAPI-dba999e3-52ec-4601-a2da-a06f3ea12dfc' # Riot Games
REGION = 'euw1' 


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " +
                     context.message.author.mention)


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


           
#client.run(os.getenv('TOKEN'))
client.run('NDQ3MDU0NTM2MTI1NzEwMzM3.Dg5vZg.cXaRGXCt4CgreyjnlZKLvQQa6Hk')
