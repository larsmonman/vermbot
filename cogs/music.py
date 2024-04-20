import discord
from discord import app_commands
from discord.ext import commands
from yt_dlp import YoutubeDL
from collections import deque


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Settings
        self.playing = False
        self.paused = False
        self.volume = 0.07
        self.vc = None

        # [song, voice_channel, text_channel]
        self.music_queue = deque()
        self.voice_channel = None
        self.YDL_OPTIONS = {'format': 'bestaudio',
                            'noplaylist': 'True', 'youtube_include_dash_manifest': False}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog loaded.')

    @app_commands.command(name="play", description="Play a song from Youtube.")
    @app_commands.describe(link="Link to the Youtube video.")
    async def play(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer(ephemeral=False)
        voice_channel = interaction.user.voice.channel
        if voice_channel is None:
            await interaction.followup.send("You must be in a Voice Channel to use this command!")
            return 0
        link=shortLinkToFulllink(link)
        song = self.search_yt(link)
        if type(song) == type(True):
            await interaction.followup.send("Could not download the song, likely a faulty URL. Try again.")
            return 0
        
        self.music_queue.append([song, voice_channel, interaction.channel])
        await interaction.followup.send(f'''"{song['title']}" added to the queue.''')
        voice_channel = None

        if self.playing == False:
            await self.play_music(interaction.user.voice.channel)

    @app_commands.command(name="pause", description="Pause the current song.")
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if self.vc == None or not self.vc.is_connected():
            await interaction.followup.send("I must be in a Voice Channel to use this command!")
            
        elif self.playing:
            self.playing = False
            self.paused = True
            self.vc.pause()
            await interaction.followup.send("Pausing...")
        elif self.paused:
            self.playing = True
            self.paused = False
            self.vc.resume()
            await interaction.followup.send("Resuming...")

    @app_commands.command(name="resume", description="Resume playing.")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if self.vc == None or not self.vc.is_connected():
            await interaction.followup.send("I must be in a Voice Channel to use this command!")

        elif self.paused:
            self.playing = True
            self.paused = False
            self.vc.resume()
            await interaction.followup.send("Resuming...")
        elif self.playing:
            await interaction.followup.send("Song is already playing!")

    @app_commands.command(name="skip", description="Skip the current song.")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if self.vc == None or not self.vc.is_connected():
            await interaction.followup.send("I must be in a Voice Channel to use this command!")
        else:
            self.vc.stop()
            self.paused = False
            await interaction.followup.send("Skipping...")
            self.play_next(interaction.user.voice.channel)

    @app_commands.command(name="queue", description="Display the current songs in queue.")
    async def queue(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        print(self.music_queue)
        q = ""
        for i in range((len(self.music_queue))):
            if i == 0:
                q += f"**Currently playing:**\n"
            elif i == 1:
                q += "**Queue:**\n"
            q += f'''"{self.music_queue[i][0]['title']}"\n'''

        if q != "":
            await interaction.followup.send(q)
        else:
            await interaction.followup.send("No music in queue.")

    @app_commands.command(name="clear", description="Stop the music and clear the queue.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if self.vc == None or not self.vc.is_connected():
            await interaction.followup.send("I must be in a Voice Channel to use this command!")
            return 0
        elif self.vc != None and self.playing:
            self.vc.stop()
        self.music_queue.clear()
        await interaction.followup.send("Clearing...")

    @app_commands.command(name="leave", description="Kick the bot from the voice channel.")
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if self.vc == None or not self.vc.is_connected():
            await interaction.followup.send("I must be in a Voice Channel to use this command!")
        else:
            self.music_queue.clear()
            self.playing = False
            self.paused = False
            await interaction.followup.send("Leaving...")
            await self.vc.disconnect()

    # Search Youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

            return {'source': info["url"], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 1:
            self.playing = True

            m_url = self.music_queue[1][0]['source']

            # Remove the last song from queue
            self.music_queue.popleft()
            print(self.music_queue)

            self.vc.play(discord.PCMVolumeTransformer(original=discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.play_next())
        else:
            self.music_queue.popleft()
            self.playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.playing = True

            m_url = self.music_queue[0][0]['source']

            # Try to connect to voice channel if it is not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                # Failed to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel.")
                    return
                
            else:
                await self.vc.move_to(self.music_queue[0][1])

            await self.music_queue[0][2].send(f'''Now playing: "{self.music_queue[0][0]['title']}"''')

            self.vc.play(discord.PCMVolumeTransformer(original=discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.play_next())
        else:
            self.playing = False

def shortLinkToFulllink(link:str):
    if "youtu.be" in link:
        location=(link.rfind("/"))+1
        link=link[location:]
        link="https://www.youtube.com/watch?v="+link
        return link
    else:
        return link

async def setup(bot):
    await bot.add_cog(Music(bot))
