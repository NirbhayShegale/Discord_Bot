import os
import threading
import time
from urllib.request import Request, urlopen
from http.server import HTTPServer, BaseHTTPRequestHandler

import discord
from llm import get_llm

# Minimal HTTP server to satisfy Render's port-binding check
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass  # suppress access logs

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

def run_keepalive():
    keepalive_url = os.environ.get("KEEPALIVE_URL") or os.environ.get("RENDER_EXTERNAL_URL")
    if not keepalive_url:
        return

    keepalive_url = keepalive_url.rstrip("/") + "/health"
    interval = int(os.environ.get("KEEPALIVE_INTERVAL", "600"))

    while True:
        try:
            request = Request(keepalive_url, method="GET")
            with urlopen(request, timeout=10) as response:
                response.read()
            print(f"Keepalive ping sent to {keepalive_url} ({response.status})")
        except Exception as error:
            print(f"Keepalive ping failed: {error}")
        time.sleep(interval)

threading.Thread(target=run_keepalive, daemon=True).start()

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
