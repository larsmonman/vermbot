from PIL import Image, ImageFont, ImageDraw
import random, pathlib
from textwrap3 import TextWrapper
import discord
from discord import app_commands
from discord.ext import commands 
import requests
import utility as utility


class Mahjong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mahjong cog loaded.')
    

    @app_commands.command(name="mahjong", description=
                          "Gets a random quote from'Awakening your Mahjong Power'")
    @app_commands.describe(img="Link to background image (leave empty for random)", 
                           text="Text to be added to the image (leave empty for random)",
                           font="Font fo text. Options: impact, magenta rose, comic sans, hieroglyphics (leave empty for random)")
    async def mahjong(self, interaction: discord.Interaction, img:str=None, text:str=None, font:str=None, color:str=None): 
        await interaction.response.defer(ephemeral=False)
        createImage(img, text, font)
        await utility.return_image(interaction)


#Creates image
def createImage(img, text, font):
        img = getBackground(img)
        text = getText(text)
        W = img.width
        H = img.height
        fontSize = int(W/20)
        #Fonts are located in the fonts folder
        font = getFont(font,fontSize)
        fill_color = (255, 255, 255)
        stroke_color = (0, 0, 0)
        drawer = ImageDraw.Draw(img)
        textLength = text.count("\n")+1
        #Scales text based on size of image and length of text
        drawer.text((int(W/5),int((H/2)-textLength*fontSize/1.75)), text, font=font, fill=fill_color, stroke_width=5, stroke_fill=stroke_color)
        img.save("images/temp/mahjongtemp.png")
        img.close()

#Gets a random quote from mahjong.txt unless another is provided, then formats it with newlines
def getText(textPlain):
        if textPlain == None:
            addQuote = True
            lines = open("mahjong.txt", encoding="utf-8").read().splitlines()
            textPlain = random.choice(lines)
        else:
             addQuote = False
        wrapper = TextWrapper()
        wrapper.width = 30
        textFormatted = "\n".join(wrapper.wrap(textPlain))
        if addQuote == True:
            textFormatted='"' + textFormatted + '"\n      - Sakurai Shouichi'
        return textFormatted

#Gets a random jpg from images/mahjong
def getBackground(img):
        if img != None:
            try:
                response = requests.get(img, timeout=5)
                print(str(response.status_code))
                if response.status_code != 200:
                    img=None
                else:
                    with open("images/temp/tempbg.png", "wb") as f:
                        f.write(response.content)
                        f.close()
                    path = "images/temp/tempbg.png"
            except requests.exceptions.RequestException:
                print("error")
                path=utility.invalidImage()
        if img == None:
            path = utility.getRanImage("images/mahjong","jpg")
        bg = Image.open(path)
        return bg

def getFont(input, fontSize):
    input=str(input)
    defaultFontPath="fonts/impact.ttf"
    if   input.lower() == "comic sans" or input.lower() == "comicsans" or input.lower() == "c" :
        path="fonts/COMICSANS.ttf"
    elif input.lower() == "hieroglyphics" or input.lower() == "h":
         path="fonts/Yiroglyphics-PKeJB.ttf"
    elif input.lower() == "Magenta Rose" or input.lower() == "magentarose" or input.lower() == "m":
         path="fonts/Magenta Rose.ttf"
    else:
         path=defaultFontPath
    return ImageFont.truetype(path, fontSize)

async def setup(bot):
    await bot.add_cog(Mahjong(bot))