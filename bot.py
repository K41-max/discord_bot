import discord
import os
import asyncio
import requests
import base64
import json
import time
from flask import Flask, request
import subprocess

# Flaskアプリを作成
app = Flask(__name__)

# Discordトークンを取得
discord_token = os.environ['DISCORD_TOKEN']

# ボットクライアントを初期化
client = discord.Client(intents=discord.Intents.default())

# メッセージの送信を行う関数
async def send_message():
    # Discordに接続
    await client.start(discord_token)

    async def get_data(username, password):
        # Basic認証のヘッダーを作成
        headers = {'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()}
        response = requests.get('https://yukibbs-server.onrender.com/bbs/admin', headers=headers)
        return response.json()

    async def main():
        username = 'admin'
        password = 'gafa074256Pass'
        last_message_content = None  # 直前のメッセージの内容を保持する変数を追加

        while True:
            data = await get_data(username, password)

            if 'main' in data:
                main_section = data['main']
                if main_section and len(main_section) > 0:
                    message_content = f"number:{main_section[0]['number']}\nname:{main_section[0]['name']}\nmessage:{main_section[0]['message']}\ninfo:{main_section[0].get('info', 'null')}\n"

                    if message_content != last_message_content:
                        # メッセージを送信
                        await client.get_channel(1217993869275168811).send(message_content)
                        last_message_content = message_content  # 送信したメッセージの内容を更新

            else:
                print("No 'main' section found in the response.")

            await asyncio.sleep(1)

    await main()

# ボットが起動したときのイベントハンドラ
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Flaskアプリのルートエンドポイント
@app.route('/', methods=['GET'])
def run_bot():
    # もしボットがすでに起動していない場合は、ボットを起動
    if not client.is_running():
        asyncio.create_task(send_message())  # ボットを非同期で起動
        return 'Bot is starting!'

    return 'Bot is already running!'

# Flaskアプリの起動
if __name__ == '__main__':
    app.run(debug=True)
