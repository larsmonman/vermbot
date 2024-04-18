import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")
        
    @commands.command(name="ping", description="Lars only")
    async def ping(self, interaction: discord.Interaction):
            await self.bot.tree.sync()
            await interaction.response.send_message("Got it boss!")

async def setup(bot):
     await bot.add_cog(ping(bot))