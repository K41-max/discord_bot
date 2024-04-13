import discord
import os
import asyncio
import requests
import base64
import json
import time
from flask import Flask

# Flaskアプリを作成
app = Flask(__name__)

# Discordトークンを取得
discord_token = os.environ['DISCORD_TOKEN']

# メッセージを送信する関数
async def send_message():
    await app.client.wait_until_ready()  # ボットが完全に起動するまで待機

    async def get_data(username, password):
        headers = {'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()}
        response = requests.get('https://yukibbs-server.onrender.com/bbs/admin', headers=headers)
        return response.json()

    username = 'admin'
    password = 'gafa074256Pass'
    last_message_content = None

    while True:
        data = await get_data(username, password)

        if 'main' in data:
            main_section = data['main']
            if main_section and len(main_section) > 0:
                message_content = f"number:{main_section[0]['number']}\nname:{main_section[0]['name']}\nmessage:{main_section[0]['message']}\ninfo:{main_section[0].get('info', 'null')}\n"

                if message_content != last_message_content:
                    await app.client.get_channel(1217993869275168811).send(message_content)
                    last_message_content = message_content

        else:
            print("No 'main' section found in the response.")

        await asyncio.sleep(1)

# Flaskアプリのルートエンドポイント
@app.route('/', methods=['GET'])
def run_bot():
    if not app.client.is_ready():
        asyncio.create_task(send_message())  # ボットを非同期で起動
        return 'Bot is starting!'

    return 'Bot is already running!'

# Discordボットのクラスを定義
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(send_message())  # ボットを起動

app.client = MyClient()  # DiscordボットのインスタンスをFlaskアプリに割り当て

# Flaskアプリの起動
if __name__ == '__main__':
    app.client.run(discord_token)  # Discordボットを起動
    app.run(debug=True)
