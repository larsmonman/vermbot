from discord.ext import commands
from discord import app_commands
import discord




class Admin(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Admin cog loaded.')
  
  @app_commands.command(name="sync", description="Lars only")
  async def sync(self, interaction: discord.Interaction):
    if interaction.user.id == 98843874872557568:
      await self.bot.tree.sync()
      print("Command tree synced.")
      await interaction.response.send_message("Got it boss!")
    else:
      await interaction.response.send_message("You must be Lars to use this command!")




async def setup(bot):
    await bot.add_cog(Admin(bot))
