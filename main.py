import discord
from discord.ext import commands
import os
import asyncio
import nest_asyncio
import cogs.helpers.setup_info as SI
import cogs.helpers.invite_functions as IF
nest_asyncio.apply()

# SETUP INFORMATION
token = SI.get_token()
bot_logo = SI.get_logo()

# SETTING INTENTS
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

# INITIALIZING BOT
client = commands.Bot(
    command_prefix='!',
    case_insnes=True,
    intents=intents,
    owner_id=SI.get_bot_owner_id()
)

client.version = '0.1.0'

# LOADING COGS
async def load_cogs():
  for filename in os.listdir('.\cogs'):
      if filename.endswith('.py'):
          print(f'Loading {filename[:-3]}...')
          await client.load_extension(f'cogs.{filename[:-3]}')
          print(f'{filename} has finished Loading!')


async def main():
  await load_cogs()

if __name__ == '__main__':
  asyncio.run(main())
  client.run(token)
