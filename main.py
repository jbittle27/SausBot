import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import platform
import DiscordUtils
import random
import os
import setupinfo as setup
import invitedata as invitedb
import asyncio

token, channel_id, server_id, rules_id, owner_id, reaction_message = setup.set_info()
new_member_role = 'New Member'
bot_logo = 'https://i.imgur.com/YKDxqOp.png'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
client = commands.Bot(
    command_prefix='!',
    case_insens=True,
    intents=intents,
    owner_id=int(owner_id)
)

tracker = DiscordUtils.InviteTracker(client)

client.version = '0.0.5'

extensions = {
    'cogs.OnEvent'
}


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    load()


@client.command()
async def stats(ctx):
    # Get the stats of the bot!
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members())
                      )  # set removes duplicates

    button = Button(label='View my Code',
                    url='https://github.com/jbittle27/SausBot')
    view = View()
    view.add_item(button)
    embed = discord.Embed(title=f'Bot Statistics',
                          description='\uFEFF',
                          url=None,
                          colour=discord.Colour(0xd9a064))

    embed.set_thumbnail(url=bot_logo)

    embed.add_field(name='Bot Version: ',
                    value=client.version, inline=False)
    embed.add_field(name='Python Version: ',
                    value=pythonVersion, inline=False)
    embed.add_field(name='Discord.Py Version: ',
                    value=dpyVersion, inline=False)
    #embed.add_field(name='Total Servers: ', value=serverCount, inline=True)
    #embed.add_field(name='Total Users: ', value=memberCount, inline=True)

    await ctx.send(embed=embed, view=view)


@client.command(aliases=['close', 'exit', 'stop'])
@commands.is_owner()
async def logout(ctx):
    # Shutdown the bot, only usable by the owner.
    await ctx.send(f'Logging out by {ctx.author.mention}\'s request. :wave:')
    await client.close()


@client.command(name='whois', aliases=['invite', 'invites'])
async def whois(ctx, arg):
    # Lookup command to find out who invited who!
    # Type !whois name#0000 to find out who invited them to the server!
    try:
        invite_object = invitedb.get_invite(f'{arg}')
        inviter = invite_object[0]
        invitee = invite_object[1]
        time = invite_object[2]
        embed = discord.Embed(title=f'{invitee} was invited by {inviter}',
                              description='', colour=discord.Colour(0xd9a064))
        embed.set_thumbnail(url=bot_logo)
        embed.add_field(
            name=f'Joined {time}', value='\uFEFF', inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send(f'Sorry, I could not find any information on {arg}')


client.run(token)
