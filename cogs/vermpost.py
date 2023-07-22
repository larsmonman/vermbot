from discord import app_commands
from discord.ext import commands, tasks
import discord
import random
import asyncpraw
import os
import datetime

time = datetime.time(hour=10, minute=00)
generals = []


class Vermpost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_post.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Vermpost cog loaded.')

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == "general":
                    generals.append(channel)
        
    @tasks.loop(time=time)
    async def daily_post(self):
        for channel in generals:
            returned_post = await get_post()
            if isinstance(returned_post, str):
                await channel.send(returned_post)
            else:
                await channel.send(embed=returned_post)


    @app_commands.command(name="verm", description="Get a random vermuth post.")
    async def get_post(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        returned_post = await get_post()
        if isinstance(returned_post, str):
            await interaction.followup.send(returned_post)
        else:
            await interaction.followup.send(embed=returned_post)





async def get_post():
    reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                              client_secret=os.getenv("client_secret"),
                              user_agent="prawer")

    subs = [
        "evangelionmemes", "tf2", "okbuddyretard",
        "jerma985", "TrueSTL", "bonehurtingjuice", "Pikmin", "Paladins"
    ]
    # subs = ["gifs"]
    filetypes = ["image", "hosted:video", "rich:video"]
    top_posts = []

    # Select a random sub, search top 15 posts for posts that contain a correct filetype
    selected_sub = random.choice(subs)
    subreddit = await reddit.subreddit(selected_sub)
    async for post in subreddit.top(time_filter="week", limit=15):
        if hasattr(post, 'post_hint'):
            hint = post.post_hint
            
            for filetype in filetypes:
                if hint == filetype:
                    top_posts.append(post)
                    break

    await reddit.close()

    selected_post = random.choice(top_posts)

    # Embed result
    if selected_post.post_hint == "image":
        em = discord.Embed(title=selected_post.title)
        em.set_image(url=selected_post.url)
        return em
    else:
        # Videos, let Discord auto-embed
        return "https://www.reddit.com/" + selected_post.permalink


async def setup(bot):
    await bot.add_cog(Vermpost(bot))
