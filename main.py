import os

import discord
from llm import get_llm

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if client.user in message.mentions:
            user_input = message.content
            user_input = user_input.replace(
                    f"<@{self.user.id}>", ""
                ).replace(
                    f"<@!{self.user.id}>", ""
                ).strip()
            response = get_llm(user_input)
            await message.channel.send(response)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  

client = MyClient(intents=intents)

client.run(os.environ.get("DISCORD_TOKEN"))
