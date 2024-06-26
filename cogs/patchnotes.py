from discord.ext import commands
from discord import app_commands
import discord

generals = []
ver = "0.2.0"

class Patchnotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Patchnotes cog loaded.')
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == "general":
                    generals.append(channel)


    @app_commands.command(name="sync", description="Lars/Runar only")
    @app_commands.describe(text="Patch notes, seperate with **")
    async def sync(self, interaction: discord.Interaction, text:str=None):
        if interaction.user.id == 98843874872557568 or interaction.user.id == 221618153376055296:
            formattedtext = "Patch notes for Vermbot version " + ver+":"
            li = list(text.split("**"))
            for x in li:
                formattedtext=formattedtext+"\n*"+x
            for channel in generals:
                msg = await channel.send(content=formattedtext)
        elif interaction.user.id == 123454594306015232:
            await interaction.response.send_message("Go fuck yourself")
        else:
            await interaction.response.send_message("You must be Lars or Runar to use this command!")


async def setup(bot):
    await bot.add_cog(Patchnotes(bot))
