import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen

import discord
from discord.ext import commands

from llm import get_llm

PORT = int(os.getenv("PORT", "8080"))
KEEPALIVE_URL = os.getenv("KEEPALIVE_URL") or os.getenv("RENDER_EXTERNAL_URL")
KEEPALIVE_INTERVAL = int(os.getenv("KEEPALIVE_INTERVAL", "300"))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass


def run_health_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
    print(f"Health server running on port {PORT}")
    server.serve_forever()


def keepalive_worker():
    if not KEEPALIVE_URL:
        print("No KEEPALIVE_URL/RENDER_EXTERNAL_URL provided; skipping keepalive.")
        return

    while True:
        try:
            with urlopen(KEEPALIVE_URL, timeout=30) as response:
                print(f"Keepalive ping successful: HTTP {response.status}")
        except Exception as exc:
            print(f"Keepalive ping failed: {exc}")
        time.sleep(KEEPALIVE_INTERVAL)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        user_input = message.content
        user_input = user_input.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
        response = get_llm(user_input)
        await message.channel.send(response)


if __name__ == "__main__":
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    keepalive_thread = threading.Thread(target=keepalive_worker, daemon=True)
    keepalive_thread.start()

    bot.run(os.getenv("DISCORD_TOKEN"))
