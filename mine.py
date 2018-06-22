import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os
import random


Client = discord.Client()
client = commands.Bot(command_prefix = '?')

@client.event # Displays the Eg. 'Playing League of Legends' message on discord.
async def on_ready():
    await client.change_presence(game=discord.Game(name =  ' running 24/7!'))
    print('Logged in as ' + client.user.name)


           
client.run(os.getenv('TOKEN'))

