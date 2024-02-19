import os
import re
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CONTEST_ADMIN_ID = int(os.getenv('CONTEST_ADMIN_ID'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def register_riot_id(message: discord.Message):
    riot_id_regex = r'!register\s([\w|\s]+#\w{1,5})$'
    compiled = re.compile(riot_id_regex)
    if compiled.match(message.content):
        riot_id = compiled.search(message.content).group(1)
        discord_user = message.author
        await message.channel.send(f'{discord_user} has registered with {riot_id} at {message.channel}!')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await register_riot_id(message)

client.run(TOKEN)