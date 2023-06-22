import random
import discord
from discord import app_commands
from discord.ext import commands
import requests
from PIL import Image


class Isaac(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Isaac cog loaded.')

    @app_commands.command(name="isaac", description="Add Isaac to a linked image.")
    @app_commands.describe(link="Link to the image.")
    async def isaac(self, interaction: discord.Interaction, link: str):
        # Get image
        await interaction.response.defer(ephemeral=False)
        response = requests.get(link)
        if response.status_code != 200:
            await interaction.followup.send("Could not fetch image.")
            return 0
        
        with open("images/temp/image.png", "wb") as f:
            f.write(response.content)
        # Edit image
        image = Image.open("images/temp/image.png")
        shortest_length = min(image.size)
        xresize = random.randint(
            int(shortest_length/12), int(shortest_length/8))
        yresize = random.randint(
            int(shortest_length/10), int(shortest_length/7))
        isaac = Image.open("images/isaacCircle.png").resize((xresize, yresize))
        xoff = random.randint(0, image.size[0]-isaac.size[0])
        yoff = random.randint(0, image.size[1]-isaac.size[1])

        image.paste(isaac, (xoff, yoff), mask=isaac)
        image.save("images/temp/image2.png")

        # Return image
        em = discord.Embed()
        file = discord.File("images/temp/image2.png")
        em.set_image(url="attachment://image2.png")
        await interaction.followup.send(file=file, embed=em)
            

async def setup(bot):
    await bot.add_cog(Isaac(bot))
