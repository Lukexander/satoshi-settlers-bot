import discord
import requests
import asyncio
import websockets
import json
from discord.ext import commands

DISCORD_TOKEN = "MTI0NTc0NzQ2OTEzMzAyNTM5MQ.GjBPhk.NS4hamu8m2osMGTTs1FFFLohHQ11PdH9fx4tWg"
DISCORD_CHANNEL_ID = 1251225028490428459


NOSTR_ENDPOINT = 'https://njump.me/npub1wz8v75sfhx2h0kggwp328ehr0aanl8c3uxzxqmxk4uvvzzm6xruqtc4qjt'

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.channel = self.get_channel(DISCORD_CHANNEL_ID)
        asyncio.create_task(self.fetch_nostr_data())

    async def fetch_nostr_data(self):
        while True:
            try:
                response = requests.get(NOSTR_ENDPOINT)
                if response.status_code == 200:
                    data = response.json()
                    await self.post_to_discord(data)
                await asyncio.sleep(60)  # Adjust the sleep time as needed
            except Exception as e:
                print(f'Error fetching data: {e}')
                await asyncio.sleep(60)

    async def post_to_discord(self, data):
        message = f"New Nostr note: {data['note']}"  # Adjust based on actual data structure
        await self.channel.send(message)


client = MyClient(intents=discord.Intents.default())
client.run(DISCORD_TOKEN)