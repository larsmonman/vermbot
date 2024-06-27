from discord.ext import commands
from discord import app_commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin cog loaded.')

    @app_commands.command(name="sync", description="Lars only")
    async def sync(self, interaction: discord.Interaction):
        if interaction.user.id == 98843874872557568 or interaction.user.id == 221618153376055296:
            await self.bot.tree.sync()
            print("Command tree synced.")
            await interaction.response.send_message("Got it boss!")
        elif interaction.user.id == 123454594306015232:
            await interaction.response.send_message("Go fuck yourself")            
        else:
            await interaction.response.send_message("You must be Lars or Runar to use this command!")

 
async def setup(bot):
    await bot.add_cog(Admin(bot))
