import random
import math
import discord
from discord import app_commands
from discord.ext import commands
import requests
from PIL import Image
from colorthief import ColorThief


class Isaac(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Isaac cog loaded.')



    @app_commands.command(name="isaac", description="Add Isaac to a linked image.")
    @app_commands.describe(link="Link to the image.")
    async def isaac(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer(ephemeral=False)
        
        # Get image
        response = requests.get(link)
        if response.status_code != 200:
            await interaction.followup.send("Could not fetch image.")
            return 0
        with open("images/temp/image.png", "wb") as f:
            f.write(response.content)
        
        dominant_color = await get_avatar(interaction)
        edit_image(Image.open("images/temp/image.png"), dominant_color)
        await return_image(interaction)

            
    @app_commands.command(name="reisaac", description="Add another Isaac to the last image.")
    async def reisaac(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        dominant_color = await get_avatar(interaction)
        edit_image(Image.open("images/temp/image2.png"), dominant_color)
        await return_image(interaction)



def edit_image(image, color):
    shortest_length = min(image.size)
    xresize = random.randint(int(shortest_length/12), int(shortest_length/8))
    yresize = random.randint(int(shortest_length/10), int(shortest_length/7))
    # Isaac
    isaac = Image.open("images/isaac.png").resize((int(xresize*0.8), int(yresize*0.8)))
    w, h = isaac.size
    
    # Get circle alpha, apply alpha to new colored image
    # Bad for performance but it works. Rework into tinting instead
    white_circle = Image.open("images/whiteCircle.png").resize((xresize, yresize))
    alpha = white_circle.getchannel('A')
    colored_circle = Image.new('RGBA', white_circle.size, color=color)
    colored_circle.putalpha(alpha) 
    
    
    # Arrow
    white_arrow = Image.open("images/whiteArrow.png").resize((xresize*2, yresize))
    # Rotate
    arrow_vector = create_vector(max(colored_circle.size))
    white_arrow = rotate_image(white_arrow, arrow_vector)
    
    alpha = white_arrow.getchannel('A')
    colored_arrow = Image.new('RGBA', white_arrow.size, color="red")
    colored_arrow.putalpha(alpha) 
    
    cw, ch = colored_circle.size
    
    colored_circle.paste(isaac,(int((cw-w)/2), int((ch-h)/2)), mask=isaac)

    xoff = random.randint(0, image.size[0]-cw)
    yoff = random.randint(0, image.size[1]-ch)

    
    image.paste(colored_circle, (xoff, yoff), mask=colored_circle)
    

    
    image.paste(colored_arrow, (int(xoff + cw/2 + arrow_vector[0]), int(yoff + arrow_vector[1])), mask=colored_arrow)
    image.save("images/temp/image2.png")
    
    
async def get_avatar(interaction):
    response = requests.get(interaction.user.avatar)
    if response.status_code != 200:
        await interaction.followup.send("Could not fetch image.")
        return 0
    with open("images/temp/avatar.png", "wb") as f:
        f.write(response.content)
        
    color_thief = ColorThief("images/temp/avatar.png")
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

async def return_image(interaction):
    em = discord.Embed()
    file = discord.File("images/temp/image2.png")
    em.set_image(url="attachment://image2.png")
    await interaction.followup.send(file=file, embed=em)
    
    
def create_vector(length):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)

    current_length = math.sqrt(x**2 + y**2)
    
    scaled_x = (x / current_length) * length
    scaled_y = (y / current_length) * length

    return (scaled_x, scaled_y)
    
    
def rotate_image(image, vector):
    angle_rad = math.atan2(vector[1], vector[0])
    angle_deg = math.degrees(angle_rad)

    rotated_image = image.rotate(angle_deg, resample=Image.BICUBIC, expand=True)

    return rotated_image
    
    
    
    
    
async def setup(bot):
    await bot.add_cog(Isaac(bot))
