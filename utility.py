import requests 
import random, pathlib
import discord
from discord import app_commands
from discord.ext import commands 

def util_test():
    print("hi")


def invalidImage():
     return getRanImage("images/error","png")

def getRanImage(path, ext):
        listofImages= list(pathlib.Path(path).glob("*."+ext))
        return random.choice(listofImages)
        
async def setup(bot):
    print("a")


async def return_image(interaction):
    em = discord.Embed()
    file = discord.File("images/temp/mahjongtemp.png")
    em.set_image(url="attachment://mahjongtemp.png")
    await interaction.followup.send(file=file, embed=em)