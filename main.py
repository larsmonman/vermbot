from discord.ext import commands
from discord import app_commands
import discord
import asyncio
import os
from dotenv.main import load_dotenv

# Misc setup
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')

# Load all cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv("TOKEN"))
        await bot.start(token)        
asyncio.run(main())


if __name__ == "__main__":
    main()
