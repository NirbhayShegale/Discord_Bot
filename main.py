import os
import discord
from discord.ext import commands
from llm import get_llm
import webserver

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
            return

    if bot.user in message.mentions:
            user_input = message.content
            user_input = user_input.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
            response = get_llm(user_input)
            await message.channel.send(response)

    
webserver.keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
