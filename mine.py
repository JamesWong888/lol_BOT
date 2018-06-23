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

champDict = {"data":{"89":{"id":89,"key":"Leona","name":"Leona","title":"the Radiant Dawn"},"110":{"id":110,"key":"Varus","name":"Varus","title":"the Arrow of Retribution"},
             "111":{"id":111,"key":"Nautilus","name":"Nautilus","title":"the Titan of the Depths"},"112":{"id":112,"key":"Viktor","name":"Viktor","title":"the Machine Herald"},
             "113":{"id":113,"key":"Sejuani","name":"Sejuani","title":"Fury of the North"},"114":{"id":114,"key":"Fiora","name":"Fiora","title":"the Grand Duelist"},
             "236":{"id":236,"key":"Lucian","name":"Lucian","title":"the Purifier"},"115":{"id":115,"key":"Ziggs","name":"Ziggs","title":"the Hexplosives Expert"},
             "117":{"id":117,"key":"Lulu","name":"Lulu","title":"the Fae Sorceress"},"90":{"id":90,"key":"Malzahar","name":"Malzahar","title":"the Prophet of the Void"},
             "238":{"id":238,"key":"Zed","name":"Zed","title":"the Master of Shadows"},"91":{"id":91,"key":"Talon","name":"Talon","title":"the Blade's Shadow"},
             "119":{"id":119,"key":"Draven","name":"Draven","title":"the Glorious Executioner"},"92":{"id":92,"key":"Riven","name":"Riven","title":"the Exile"},
             "516":{"id":516,"key":"Ornn","name":"Ornn","title":"The Fire below the Mountain"},"96":{"id":96,"key":"KogMaw","name":"Kog'Maw","title":"the Mouth of the Abyss"},
             "10":{"id":10,"key":"Kayle","name":"Kayle","title":"The Judicator"},"98":{"id":98,"key":"Shen","name":"Shen","title":"the Eye of Twilight"},
             "99":{"id":99,"key":"Lux","name":"Lux","title":"the Lady of Luminosity"},"11":{"id":11,"key":"MasterYi","name":"Master Yi","title":"the Wuju Bladesman"},
             "12":{"id":12,"key":"Alistar","name":"Alistar","title":"the Minotaur"},"13":{"id":13,"key":"Ryze","name":"Ryze","title":"the Rune Mage"},
             "14":{"id":14,"key":"Sion","name":"Sion","title":"The Undead Juggernaut"},"15":{"id":15,"key":"Sivir","name":"Sivir","title":"the Battle Mistress"},
             "16":{"id":16,"key":"Soraka","name":"Soraka","title":"the Starchild"},"17":{"id":17,"key":"Teemo","name":"Teemo","title":"the Swift Scout"},
             "18":{"id":18,"key":"Tristana","name":"Tristana","title":"the Yordle Gunner"},"19":{"id":19,"key":"Warwick","name":"Warwick","title":"the Uncaged Wrath of Zaun"},
             "240":{"id":240,"key":"Kled","name":"Kled","title":"the Cantankerous Cavalier"},"120":{"id":120,"key":"Hecarim","name":"Hecarim","title":"the Shadow of War"},
             "121":{"id":121,"key":"Khazix","name":"Kha'Zix","title":"the Voidreaver"},"1":{"id":1,"key":"Annie","name":"Annie","title":"the Dark Child"},
             "122":{"id":122,"key":"Darius","name":"Darius","title":"the Hand of Noxus"},"2":{"id":2,"key":"Olaf","name":"Olaf","title":"the Berserker"},
             "245":{"id":245,"key":"Ekko","name":"Ekko","title":"the Boy Who Shattered Time"},"3":{"id":3,"key":"Galio","name":"Galio","title":"the Colossus"},
             "4":{"id":4,"key":"TwistedFate","name":"Twisted Fate","title":"the Card Master"},"126":{"id":126,"key":"Jayce","name":"Jayce","title":"the Defender of Tomorrow"},
             "5":{"id":5,"key":"XinZhao","name":"Xin Zhao","title":"the Seneschal of Demacia"},"127":{"id":127,"key":"Lissandra","name":"Lissandra","title":"the Ice Witch"},
             "6":{"id":6,"key":"Urgot","name":"Urgot","title":"the Dreadnought"},"7":{"id":7,"key":"Leblanc","name":"LeBlanc","title":"the Deceiver"},
             "8":{"id":8,"key":"Vladimir","name":"Vladimir","title":"the Crimson Reaper"},"9":{"id":9,"key":"Fiddlesticks","name":"Fiddlesticks","title":"the Harbinger of Doom"},
             "20":{"id":20,"key":"Nunu","name":"Nunu","title":"the Yeti Rider"},"21":{"id":21,"key":"MissFortune","name":"Miss Fortune","title":"the Bounty Hunter"},
             "22":{"id":22,"key":"Ashe","name":"Ashe","title":"the Frost Archer"},"23":{"id":23,"key":"Tryndamere","name":"Tryndamere","title":"the Barbarian King"},
             "24":{"id":24,"key":"Jax","name":"Jax","title":"Grandmaster at Arms"},"25":{"id":25,"key":"Morgana","name":"Morgana","title":"Fallen Angel"},
             "26":{"id":26,"key":"Zilean","name":"Zilean","title":"the Chronokeeper"},"27":{"id":27,"key":"Singed","name":"Singed","title":"the Mad Chemist"},
             "28":{"id":28,"key":"Evelynn","name":"Evelynn","title":"Agony's Embrace"},"29":{"id":29,"key":"Twitch","name":"Twitch","title":"the Plague Rat"},
             "131":{"id":131,"key":"Diana","name":"Diana","title":"Scorn of the Moon"},"133":{"id":133,"key":"Quinn","name":"Quinn","title":"Demacia's Wings"},
             "254":{"id":254,"key":"Vi","name":"Vi","title":"the Piltover Enforcer"},"497":{"id":497,"key":"Rakan","name":"Rakan","title":"The Charmer"},
             "134":{"id":134,"key":"Syndra","name":"Syndra","title":"the Dark Sovereign"},"498":{"id":498,"key":"Xayah","name":"Xayah","title":"the Rebel"},
             "136":{"id":136,"key":"AurelionSol","name":"Aurelion Sol","title":"The Star Forger"},"412":{"id":412,"key":"Thresh","name":"Thresh","title":"the Chain Warden"},
             "30":{"id":30,"key":"Karthus","name":"Karthus","title":"the Deathsinger"},"31":{"id":31,"key":"Chogath","name":"Cho'Gath","title":"the Terror of the Void"},
             "32":{"id":32,"key":"Amumu","name":"Amumu","title":"the Sad Mummy"},"33":{"id":33,"key":"Rammus","name":"Rammus","title":"the Armordillo"},
             "34":{"id":34,"key":"Anivia","name":"Anivia","title":"the Cryophoenix"},"35":{"id":35,"key":"Shaco","name":"Shaco","title":"the Demon Jester"},
             "36":{"id":36,"key":"DrMundo","name":"Dr. Mundo","title":"the Madman of Zaun"},"37":{"id":37,"key":"Sona","name":"Sona","title":"Maven of the Strings"},
             "38":{"id":38,"key":"Kassadin","name":"Kassadin","title":"the Void Walker"},"39":{"id":39,"key":"Irelia","name":"Irelia","title":"the Blade Dancer"},
             "141":{"id":141,"key":"Kayn","name":"Kayn","title":"the Shadow Reaper"},"142":{"id":142,"key":"Zoe","name":"Zoe","title":"the Aspect of Twilight"},
             "143":{"id":143,"key":"Zyra","name":"Zyra","title":"Rise of the Thorns"},"266":{"id":266,"key":"Aatrox","name":"Aatrox","title":"the Darkin Blade"},
             "420":{"id":420,"key":"Illaoi","name":"Illaoi","title":"the Kraken Priestess"},"145":{"id":145,"key":"Kaisa","name":"Kai'Sa","title":"Daughter of the Void"},
             "267":{"id":267,"key":"Nami","name":"Nami","title":"the Tidecaller"},"421":{"id":421,"key":"RekSai","name":"Rek'Sai","title":"the Void Burrower"},
             "268":{"id":268,"key":"Azir","name":"Azir","title":"the Emperor of the Sands"},"427":{"id":427,"key":"Ivern","name":"Ivern","title":"the Green Father"},
             "429":{"id":429,"key":"Kalista","name":"Kalista","title":"the Spear of Vengeance"},"40":{"id":40,"key":"Janna","name":"Janna","title":"the Storm's Fury"},
             "41":{"id":41,"key":"Gangplank","name":"Gangplank","title":"the Saltwater Scourge"},"42":{"id":42,"key":"Corki","name":"Corki","title":"the Daring Bombardier"},
             "43":{"id":43,"key":"Karma","name":"Karma","title":"the Enlightened One"},"44":{"id":44,"key":"Taric","name":"Taric","title":"the Shield of Valoran"},
             "45":{"id":45,"key":"Veigar","name":"Veigar","title":"the Tiny Master of Evil"},"48":{"id":48,"key":"Trundle","name":"Trundle","title":"the Troll King"},
             "150":{"id":150,"key":"Gnar","name":"Gnar","title":"the Missing Link"},"154":{"id":154,"key":"Zac","name":"Zac","title":"the Secret Weapon"},
             "432":{"id":432,"key":"Bard","name":"Bard","title":"the Wandering Caretaker"},"157":{"id":157,"key":"Yasuo","name":"Yasuo","title":"the Unforgiven"},
             "50":{"id":50,"key":"Swain","name":"Swain","title":"the Noxian Grand General"},"51":{"id":51,"key":"Caitlyn","name":"Caitlyn","title":"the Sheriff of Piltover"},
             "53":{"id":53,"key":"Blitzcrank","name":"Blitzcrank","title":"the Great Steam Golem"},"54":{"id":54,"key":"Malphite","name":"Malphite","title":"Shard of the Monolith"},
             "55":{"id":55,"key":"Katarina","name":"Katarina","title":"the Sinister Blade"},"56":{"id":56,"key":"Nocturne","name":"Nocturne","title":"the Eternal Nightmare"},
             "57":{"id":57,"key":"Maokai","name":"Maokai","title":"the Twisted Treant"},"58":{"id":58,"key":"Renekton","name":"Renekton","title":"the Butcher of the Sands"},
             "59":{"id":59,"key":"JarvanIV","name":"Jarvan IV","title":"the Exemplar of Demacia"},"161":{"id":161,"key":"Velkoz","name":"Vel'Koz","title":"the Eye of the Void"},
             "163":{"id":163,"key":"Taliyah","name":"Taliyah","title":"the Stoneweaver"},"164":{"id":164,"key":"Camille","name":"Camille","title":"the Steel Shadow"},
             "201":{"id":201,"key":"Braum","name":"Braum","title":"the Heart of the Freljord"},"202":{"id":202,"key":"Jhin","name":"Jhin","title":"the Virtuoso"},
             "203":{"id":203,"key":"Kindred","name":"Kindred","title":"The Eternal Hunters"},"60":{"id":60,"key":"Elise","name":"Elise","title":"the Spider Queen"},
             "61":{"id":61,"key":"Orianna","name":"Orianna","title":"the Lady of Clockwork"},"62":{"id":62,"key":"MonkeyKing","name":"Wukong","title":"the Monkey King"},
             "63":{"id":63,"key":"Brand","name":"Brand","title":"the Burning Vengeance"},"64":{"id":64,"key":"LeeSin","name":"Lee Sin","title":"the Blind Monk"},
             "67":{"id":67,"key":"Vayne","name":"Vayne","title":"the Night Hunter"},"68":{"id":68,"key":"Rumble","name":"Rumble","title":"the Mechanized Menace"},
             "69":{"id":69,"key":"Cassiopeia","name":"Cassiopeia","title":"the Serpent's Embrace"},"72":{"id":72,"key":"Skarner","name":"Skarner","title":"the Crystal Vanguard"},
             "74":{"id":74,"key":"Heimerdinger","name":"Heimerdinger","title":"the Revered Inventor"},"75":{"id":75,"key":"Nasus","name":"Nasus","title":"the Curator of the Sands"},
             "76":{"id":76,"key":"Nidalee","name":"Nidalee","title":"the Bestial Huntress"},"77":{"id":77,"key":"Udyr","name":"Udyr","title":"the Spirit Walker"},
             "78":{"id":78,"key":"Poppy","name":"Poppy","title":"Keeper of the Hammer"},"79":{"id":79,"key":"Gragas","name":"Gragas","title":"the Rabble Rouser"},
             "222":{"id":222,"key":"Jinx","name":"Jinx","title":"the Loose Cannon"},"101":{"id":101,"key":"Xerath","name":"Xerath","title":"the Magus Ascendant"},
             "102":{"id":102,"key":"Shyvana","name":"Shyvana","title":"the Half-Dragon"},"223":{"id":223,"key":"TahmKench","name":"Tahm Kench","title":"the River King"},
             "103":{"id":103,"key":"Ahri","name":"Ahri","title":"the Nine-Tailed Fox"},"104":{"id":104,"key":"Graves","name":"Graves","title":"the Outlaw"},
             "105":{"id":105,"key":"Fizz","name":"Fizz","title":"the Tidal Trickster"},"106":{"id":106,"key":"Volibear","name":"Volibear","title":"the Thunder's Roar"},
             "80":{"id":80,"key":"Pantheon","name":"Pantheon","title":"the Artisan of War"},"107":{"id":107,"key":"Rengar","name":"Rengar","title":"the Pridestalker"},
             "81":{"id":81,"key":"Ezreal","name":"Ezreal","title":"the Prodigal Explorer"},"82":{"id":82,"key":"Mordekaiser","name":"Mordekaiser","title":"the Iron Revenant"},
             "83":{"id":83,"key":"Yorick","name":"Yorick","title":"Shepherd of Souls"},"84":{"id":84,"key":"Akali","name":"Akali","title":"the Fist of Shadow"},
             "85":{"id":85,"key":"Kennen","name":"Kennen","title":"the Heart of the Tempest"},
             "86":{"id":86,"key":"Garen","name":"Garen","title":"The Might of Demacia"}},"type":"champion","version":"8.10.1"}



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
    await client.say("Success!2")
    
    for counter in range(14):
        champID = responseJSON['champions'][counter]['id']
        await client.say(champID) 
        champName = champDict['data'][str(champID)]['key']
        await client.say(champName) 
        champTitle = champDict['data'][str(champID)]['title'] # Eg. Lux:   The Lady of Luminosity
        await client.say(champTitle)
        printQueue.append('{:15}{:10}'.format(champName, champTitle))
        await client.say(printQueue)

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

