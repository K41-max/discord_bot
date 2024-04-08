import discord
import os
import asyncio
import requests
import base64
import json
import time

# クライアントを作成
client = discord.Client(intents=discord.Intents.default())

discord_token = os.environ['DISCORD_TOKEN']

# メッセージを送信する関数
async def send_message():
    # メッセージを送信するチャンネルを取得
    channel = client.get_channel(1217993869275168811)

    async def get_data(username, password):
        # Basic認証のヘッダーを作成
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
                if main_section and len(main_section) > 0:
                    current_number = int(main_section[0]['number'])

                    if last_number is None or current_number != last_number:
                        info = main_section[0].get('info', 'null')  # info キーが存在しない場合は 'null' を返す
                        await channel.send(f"\n\nnumber:{current_number}\nname:{main_section[0]['name']}\nmessage:{main_section[0]['message']}\ninfo:{info}\n")

                        last_number = current_number  # メッセージが送信されたら last_number を更新

            else:
                print("No 'main' section found in the response.")

            await asyncio.sleep(1)

    await main()

# ボットが起動したときのイベントハンドラ
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # メッセージを送信するタスクを開始
    await send_message()

# Discordに接続する
client.run(discord_token)
