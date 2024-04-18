from PIL import Image, ImageFont, ImageDraw
import random, pathlib
from textwrap3 import TextWrapper
import discord
from discord import app_commands
from discord.ext import commands 


class Mahjong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mahjong cog loaded.')    

    @app_commands.command(name="mahjong", description=
                          "Gets a random quote from'Awakening your Mahjong Power'")
    async def mahjong(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        createImage()
        await return_image(interaction)

#Returns image as a response to user
async def return_image(interaction):
    em = discord.Embed()
    file = discord.File("images/temp/mahjongtemp.png")
    em.set_image(url="attachment://mahjongtemp.png")
    await interaction.followup.send(file=file, embed=em)

#Creates image
def createImage():
        img = getBackground()
        text = getText()
        W = img.width
        H = img.height
        fontSize = int(W/20)
        #Fonts are located in the fonts folder
        font = ImageFont.truetype("fonts/impact.ttf", fontSize)
        fill_color = (255, 255, 255)
        stroke_color = (0, 0, 0)
        drawer = ImageDraw.Draw(img)
        textLength = text.count("\n")+1
        #Scales text based on size of image and length of text
        drawer.text((int(W/5),int((H/2)-textLength*fontSize/1.75)), text, font=font, fill=fill_color, stroke_width=5, stroke_fill=stroke_color)
        img.save("images/temp/mahjongtemp.png")
        img.close()

#Gets a random quote from mahjong.txt, then formats it with newlines
def getText():
        lines = open("mahjong.txt", encoding="utf-8").read().splitlines()
        textPlain = random.choice(lines)
        wrapper = TextWrapper()
        wrapper.width = 30
        textFormatted = "\n".join(wrapper.wrap(textPlain))
        return textFormatted

#Gets a random jpg from images/mahjong
def getBackground():
        listofImages= list(pathlib.Path("images/mahjong").glob("*.jpg"))    
        random.choice(listofImages)
        img = Image.open(random.choice(listofImages))
        return img


async def setup(bot):
    await bot.add_cog(Mahjong(bot))