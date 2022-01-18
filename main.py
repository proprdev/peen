import discord, logging
from cogs.userinfo import UserInfo
from cogs.voice import Voice
from os import getenv
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)

intents = discord.Intents.default()
client = discord.Bot()

token: str

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.add_cog(UserInfo(client))
client.add_cog(Voice(client))

load_dotenv()
token = getenv("TOKEN")

client.run(token)