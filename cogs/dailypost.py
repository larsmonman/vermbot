from discord.ext import commands, tasks
from discord import app_commands
import discord
import random
import asyncpraw
import os
import datetime

time = datetime.time(hour=10, minute=00)
generals=[]


class Dailypost(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Dailypost cog loaded.')
  
    for guild in self.bot.guilds:
      for channel in guild.text_channels:
        if channel.name == "general":
          generals.append(channel)
    
    self.dailypost.start()
    
  @tasks.loop(time=time)
  async def dailypost(self):
    for channel in generals:
      await channel.send(embed = await get_post())
      
      
  @app_commands.command(name = "verm", description = "Get a random vermuth post")
  async def dailypost(self, interaction: discord.Interaction):
    await interaction.response.send_message(embed = await get_post())


async def get_post():
  reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                            client_secret=os.getenv("client_secret"),
                            user_agent="prawer")

  subs = [
    "evangelionmemes", "tf2", "smite", "okbuddyretard",
    "jerma985", "greentext", "okbuddyfortnite", "TrueSTL", "bonehurtingjuice", "whenthe", "Pikmin"
  ]
  filetypes = [".png", ".jpg", ".gif", ".mp4", ".webm"]
  top_posts = []

  #Select a random sub, search top 30 posts for posts that contain a correct filetype
  selected_sub = random.choice(subs)
  subreddit = await reddit.subreddit(selected_sub)
  async for post in subreddit.top(time_filter="month", limit=30):
    for filetype in filetypes:
      if post.url.endswith(filetype):
        top_posts.append(post)
        break

  await reddit.close()
  
  selected_post = random.choice(top_posts)

  #Embed result
  em = discord.Embed(title=selected_post.title)
  em.set_image(url=selected_post.url)

  return em


async def setup(bot):
    await bot.add_cog(Dailypost(bot))
