from PIL import Image
import face_recognition
from PIL import Image, ImageDraw, ImageFilter
import discord
from discord import app_commands
from discord.ext import commands
import requests
import random, pathlib


class Pingafy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):   
        print('Pingafy cog loaded.')

    @app_commands.command(name="pingafy", description="Adds pingas to persons face (currently only works with real life looking faces).")
    @app_commands.describe(link="Link to the image.")
    async def isaac(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer(ephemeral=False)
        response = requests.get(link)
        if response.status_code != 200:
            await interaction.followup.send("Could not fetch image.")
            return 0
        with open("images/temp/imagetopingafy.png", "wb") as f:
            f.write(response.content)
        if pingafyImage() == 0:
            await randomPingas(interaction)
        else:
            await send_pingas(interaction)

async def send_pingas(interaction):
    em = discord.Embed()
    file = discord.File("images/temp/pingastemp.png")
    em.set_image(url="attachment://pingastemp.png")
    await interaction.followup.send(file=file, embed=em)

def pingafyImage():
    facerec = face_recognition.load_image_file("images/temp/imagetopingafy.png")
    face_locations = face_recognition.face_locations(facerec)
    if not face_locations:
        return 0
    image = Image.open('images/temp/imagetopingafy.png')
    pingas = Image.open('images/pingas.png')
    for face_location in face_locations:
        top, right, bottom, left = face_location
    pW=pingas.width
    pH=pingas.height
    pRatio = pW/pH
    sizeDiffH=bottom-top
    pNewH = int((sizeDiffH)*1.2)
    pNewW = int((pRatio*sizeDiffH)*1.2)
    pX = int(left-(sizeDiffH*0.3))
    pY = int(top-(sizeDiffH*0.3))
    pingas = pingas.resize((pNewW,pNewH))
    image.paste(pingas, (pX, pY), pingas)
    image.save("images/temp/pingastemp.png")
    image.close()
    return 1

async def randomPingas(interaction):
    listofImages= list(pathlib.Path("images/eggman").glob("*.jpg"))    
    random.choice(listofImages)
    em = discord.Embed()
    file = discord.File(random.choice(listofImages))
    em.set_image(url="attachment://eggman")
    errorMsg = "Could not find any face to pingafy"
    await interaction.followup.send(content = errorMsg, file=file)

async def setup(bot):
    await bot.add_cog(Pingafy(bot))
