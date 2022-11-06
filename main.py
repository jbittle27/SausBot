import discord
from discord.ext import commands
from discord import app_commands
import DiscordUtils
import random
import os
import setup as sp

token = sp.get_token()
channel_id, server_id = sp.get_data()
prefix = "!"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents)
tracker = DiscordUtils.InviteTracker(client)


@client.event
async def on_ready():
    pass
    # await client.send_message(discord.Object(id=channel_id), 'working')


@client.event
async def on_member_join(new_member):
    inviter = await tracker.fetch_inviter(new_member)
    with open('invites.txt', 'a') as f:
        f.write(f'{new_member}, {inviter}, {new_member.joined_at}\n')
    channel = client.get_channel(int(channel_id))
    await channel.send(f'{inviter} invited {new_member}!')


@client.command()
async def invite(ctx, arg):
    with open('invites.txt', 'r') as f:
        file_lines = f.readlines()
        # quick getaround for a user being invited multiple times
        # will get the most recent invite added
        for line in reversed(file_lines):
            if arg == line.split(',')[0]:
                inviter = line.split(',')[1]
                await ctx.send(f'{inviter} invited {arg}!')
                break


client.run(token)
