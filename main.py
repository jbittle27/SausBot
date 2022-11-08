import discord
from discord.ext import commands
from discord import app_commands
import logging
from pathlib import Path
import platform
import DiscordUtils
import random
import os
import setup as sp
import invitedata as invitedb

cwd = Path(__file__).parents[0]
cwd = str(cwd)
token = sp.get_token()
channel_id, server_id, rules_id, owner_id = sp.get_data()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(
    command_prefix='!',
    case_insens=True,
    intents=intents,
    owner_id=int(owner_id)
)

tracker = DiscordUtils.InviteTracker(client)

client.version = '0.0.3'


@client.event
async def on_command_error(ctx, error):
    # Ignore these errors
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)

        if int(h) is 0 and int(m) is 0:
            await ctx.send(f'You must wait {int(s)} seconds to use this command!')
        elif int(h) is 0 and int(m) is not 0:
            await ctx.send(f'You must wait {int(n)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes, and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f'Sorry @{ctx.author.mention}, you lack the permission to use this command.')
    raise error


@client.event
async def on_message(message):
    # ignore ourselves
    if message.author.id == client.user.id:
        return

    await client.process_commands(message)


# Bot Stats Command
@client.command()
async def stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))  # set removes duplicates

    embed = discord.Embed(title=f'Bot Statistics',
                          description='\uFEFF',
                          url='https://github.com/jbittle27/new-discord-bot',
                          colour=discord.Colour(0xd9a064))

    embed.set_thumbnail(url='https://i.imgur.com/YKDxqOp.png')

    embed.add_field(name='Bot Version: ', value=client.version, inline=False)
    embed.add_field(name='Python Version: ', value=pythonVersion, inline=False)
    embed.add_field(name='Discord.Py Version: ',
                    value=dpyVersion, inline=False)
    embed.add_field(name='Total Servers: ', value=serverCount, inline=True)
    embed.add_field(name='Total Users: ', value=memberCount, inline=True)

    embed.set_footer(text=f'Created by | fauX')

    await ctx.send(embed=embed)


@client.command(aliases=['close', 'exit', 'stop'])
@commands.is_owner()
async def logout(ctx):
    '''
    If the user running the command owns the bot, then the bot will be disconnected.
    '''

    await ctx.send(f'Logging out by {ctx.author.mention}\'s request. :wave:')
    await client.close()


@client.event
async def on_member_remove(member):
    invitedb.remove_invite(member)


@client.event
async def on_member_join(new_member):
    inviter = await tracker.fetch_inviter(new_member)
    invitedb.add_invite(f'{inviter}', f'{new_member}')


@client.command(name='invite', aliases=['Invite', 'invites', 'Invites'])
async def invite(ctx, arg):
    try:
        invite_object = invitedb.get_invite(f'{arg}')
        inviter = invite_object[0]
        invitee = invite_object[1]
        time = invite_object[2]
        embed = discord.Embed(title=f'{invitee} was invited by {inviter}',
                              description='',
                              colour=discord.Colour(0xd9a064))

        embed.set_thumbnail(url='https://i.imgur.com/YKDxqOp.png')

        embed.add_field(name=f'Date:',
                        value=f'{invitee} joined at {time}', inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send(f'Sorry, I could not find any information on {arg}')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f'Use ! to interact with me.'))


client.run(token)
