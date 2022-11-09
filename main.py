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
tacobell_logo = 'https://i.imgur.com/YKDxqOp.png'

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


@client.event
async def on_raw_reaction_add(ctx):
    guild_id = ctx.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, name=new_member_role)
    channel = client.get_channel(ctx.channel_id)
    message = await channel.fetch_message(ctx.message_id)
    user = client.get_user(ctx.user_id)
    user_emoji = ctx.emoji

    if user_emoji.name == '✅':
        if role is not None:
            member = discord.utils.find(
                lambda m: m.id == ctx.user_id, guild.members)
            if member is not None:
                try:
                    await member.add_roles(role)
                    await message.remove_reaction('✅', user)
                except:
                    print('Error adding role to user')
                    return
    else:
        try:
            member = discord.utils.find(
                lambda m: m.id == ctx.user_id, guild.members)
            await message.remove_reaction(user_emoji, user)
        except:
            print('Error removing unknown emoji')
            return


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f'Use ! to interact with me.'))


@client.event
async def on_command_error(ctx, error):
    # Ignore these errors
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)

        if int(h) == 0 and int(m) == 0:
            await ctx.send(f'You must wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f'You must wait {int(n)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes, and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f'Sorry @{ctx.author.mention}, you lack the permission to use this command.')
    raise error


@client.event
async def on_member_join(new_member):
    # When a member joins, save inviter, member, and time into db
    inviter = await tracker.fetch_inviter(new_member)
    invitedb.add_invite(f'{inviter}', f'{new_member}')
    return


@client.event
async def on_member_remove(member):
    # When a member leaves, remove invite information from db
    invitedb.remove_invite(member)
    return


@client.event
async def on_message(message):
    # On Message Events
    # Ignore bot messages
    if message.author.id == client.user.id:
        return

    await client.process_commands(message)


@client.command()
async def stats(ctx):
    # Get the stats of the bot!
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members())
                      )  # set removes duplicates

    embed = discord.Embed(title=f'Bot Statistics',
                          description='\uFEFF',
                          url='https://github.com/jbittle27/SausBot',
                          colour=discord.Colour(0xd9a064))

    embed.set_thumbnail(url=tacobell_logo)

    embed.add_field(name='Bot Version: ',
                    value=client.version, inline=False)
    embed.add_field(name='Python Version: ',
                    value=pythonVersion, inline=False)
    embed.add_field(name='Discord.Py Version: ',
                    value=dpyVersion, inline=False)
    embed.add_field(name='Total Servers: ', value=serverCount, inline=True)
    embed.add_field(name='Total Users: ', value=memberCount, inline=True)

    await ctx.send(embed=embed)


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
        embed.set_thumbnail(url=tacobell_logo)
        embed.add_field(
            name=f'Joined {time}', value='\uFEFF', inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send(f'Sorry, I could not find any information on {arg}')


client.run(token)
