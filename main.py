import discord
import os
import asyncio
import requests
import base64
import json
import time
from keep import keep_alive  # Assuming keep_alive function is defined in keep.py

# Create a client
client = discord.Client(intents=discord.Intents.default())

discord_token = os.environ['DISCORD_TOKEN']

# Function to send messages
async def send_message():
    # Get the channel to send messages
    channel = client.get_channel(1217993869275168811)

    async def get_data(username, password):
        # Create Basic Authentication headers
        headers = {'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()}
        response = requests.get('https://yukibbs-server.onrender.com/bbs/admin', headers=headers)
        return response.json()

    async def main():
        username = 'admin'
        password = 'gafa074256Pass'
        last_number = None

        while True:
            data = await get_data(username, password)

            if 'main' in data:
                main_section = data['main']
                if main_section:
                    current_number = int(main_section[0]['number'])

                    if last_number is not None and current_number != last_number:
                        info = main_section[0]['info']
                        if not info:  # if info is empty
                            info = "null"

                        await channel.send(f"\n\nnumber:{current_number}\nname:{main_section[0]['name']}\nmessage:{main_section[0]['message']}\ninfo:{info}\n")

                    last_number = current_number

            else:
                print("No 'main' section found in the response.")

            await asyncio.sleep(1)

    await main()

# Event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Start the task to send messages
    await send_message()

# Connect to Discord
keep_alive()

try:
    client.run(discord_token)
except:
    os.system("kill")
