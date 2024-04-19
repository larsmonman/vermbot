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

    #Listens for command, takes an URL to an image as an argument
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
            #No face was located in the imgage
            await randomPingas(interaction)
        else:
            #Respond with image
            await send_pingas(interaction)

async def send_pingas(interaction):
    em = discord.Embed()
    file = discord.File("images/temp/pingastemp.png")
    em.set_image(url="attachment://pingastemp.png")
    await interaction.followup.send(file=file, embed=em)

def pingafyImage():
    #Locates image in face and creates a list with locations of the face in the image
    facerec = face_recognition.load_image_file("images/temp/imagetopingafy.png")
    face_locations = face_recognition.face_locations(facerec)
    if not face_locations:
        #If no face was found in the image
        return 0
    #Loads image objects
    image = Image.open('images/temp/imagetopingafy.png')
    pingas = Image.open('images/pingas.png')
    #Declaring variables from location list
    #Top is the topmost pixel of the eyes of  the face, bottom is the chin, left and right is around the chin  
    for face_location in face_locations:
        top, right, bottom, left = face_location
    #Scaling the pingas image
    pW=pingas.width
    pH=pingas.height
    pRatio = pW/pH
    sizeDiffH=bottom-top
    pNewH = int((sizeDiffH)*1.2)
    pNewW = int((pRatio*sizeDiffH)*1.2)
    pingas = pingas.resize((pNewW,pNewH))

    #Since the pingas image include a mustache, and is fairly tall, we add a negative offset to where the face is places 
    pX = int(left-(sizeDiffH*0.3))
    pY = int(top-(sizeDiffH*0.3))

    image.paste(pingas, (pX, pY), pingas)
    image.save("images/temp/pingastemp.png")
    image.close()
    pingas.close()
    return 1

async def randomPingas(interaction):
    #Sends a funny image if we can't find a face- 
    listofImages= list(pathlib.Path("images/eggman").glob("*.jpg"))    
    random.choice(listofImages)
    em = discord.Embed()
    file = discord.File(random.choice(listofImages))
    em.set_image(url="attachment://eggman")
    errorMsg = "Could not find any face to pingafy"
    await interaction.followup.send(content = errorMsg, file=file)

async def setup(bot):
    await bot.add_cog(Pingafy(bot))
