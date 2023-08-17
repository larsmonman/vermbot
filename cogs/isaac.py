import random
import math
import discord
from discord import app_commands
from discord.ext import commands
import requests
from PIL import Image
from colorthief import ColorThief
import numpy as np
import colorsys


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



async def get_avatar(interaction):
    response = requests.get(interaction.user.avatar)
    if response.status_code != 200:
        await interaction.followup.send("Could not fetch image.")
        return 0
    with open("images/temp/avatar.png", "wb") as f:
        f.write(response.content)
        
    color_thief = ColorThief("images/temp/avatar.png")
    dominant_color = color_thief.get_color(quality=3)
    return dominant_color


def edit_image(image, color):
    # Resize images based on the input's shortest side
    shortest_length = min(image.size)
    xresize = random.randint(int(shortest_length/12), int(shortest_length/8))
    yresize = random.randint(int(shortest_length/10), int(shortest_length/7))
    
    red_circle = Image.open("images/redCircle.png").resize((xresize, yresize))
    isaac = Image.open("images/isaac.png").resize((int(xresize*0.8), int(yresize*0.8)))
    tinted_isaac = tint(isaac, color)
    
    # Paste Isaac into middle of circle
    cw, ch = red_circle.size
    iw, ih = tinted_isaac.size
    red_circle.paste(tinted_isaac,(int((cw-iw)/2), int((ch-ih)/2)), mask=tinted_isaac)
    
    # Place circle somewhere the entire circle is visible
    xoff = random.randint(0, image.size[0]-cw)
    yoff = random.randint(0, image.size[1]-ch)
    image.paste(red_circle, (xoff, yoff), mask=red_circle)

    red_arrow = Image.open("images/redArrow.png").resize((int(xresize*6), int(yresize/2)))
    arrow_vector = create_vector(red_circle.size)
    angle_rad = math.atan2(arrow_vector[1], arrow_vector[0])
    angle_deg = math.degrees(angle_rad)
    rotated_arrow = red_arrow.rotate(angle_deg, expand=True)
    
    c_center = (int(xoff + cw/2), int(yoff + ch/2))
    image.paste(rotated_arrow, (int(c_center[0] - rotated_arrow.width/2 + arrow_vector[0]/2),
                                int(c_center[1] - rotated_arrow.height/2 - arrow_vector[1]/2)), mask=rotated_arrow)
    image.save("images/temp/image2.png")
    
async def return_image(interaction):
    em = discord.Embed()
    file = discord.File("images/temp/image2.png")
    em.set_image(url="attachment://image2.png")
    await interaction.followup.send(file=file, embed=em)
    
# Takes circle size and creates a random vector for where to place the arrow pointing at Isaac, based on circle's longest side
def create_vector(circle_size):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    current_length = math.sqrt(x**2 + y**2)
    scaled_x = (x / current_length) * max(circle_size)
    scaled_y = (y / current_length) * max(circle_size)
    return (scaled_x, scaled_y)
    
def set_hs(arr, hout, sout):
    
    rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
    hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)
    
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    s = sout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def tint(image, color):
    hue, sat, v = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    
    img = image.convert('RGBA')
    arr = np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(set_hs(arr, hue, sat/2).astype('uint8'), 'RGBA')

    return new_img
    
    
async def setup(bot):
    await bot.add_cog(Isaac(bot))
