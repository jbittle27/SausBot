import inspect
import os
import random
import DiscordUtils
import platform
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
import discord
from .helpers import setup_info as SI
from .helpers import invite_functions as IF
import asyncio


class OnCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reaction_message = SI.get_reaction_message_id
        self.verification_role = SI.get_verification_role()
        self.logo = SI.get_logo()
        self.tracker = DiscordUtils.InviteTracker(self.client)

    @commands.command()
    async def stats(self, ctx):
        # Get the stats of the bot!
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members())
                          )  # set removes duplicates

        button = Button(label='View my Code!',
                        url='https://github.com/jbittle27/SausBot')
        view = View()
        view.add_item(button)
        embed = discord.Embed(title=f'Bot Statistics',
                              description='\uFEFF',
                              url=None,
                              colour=discord.Colour(0xd9a064))

        embed.set_thumbnail(url=self.logo)

        embed.add_field(name='Bot Version: ',
                        value=self.client.version, inline=False)
        embed.add_field(name='Python Version: ',
                        value=pythonVersion, inline=False)
        embed.add_field(name='Discord.Py Version: ',
                        value=dpyVersion, inline=False)
        #embed.add_field(name='Total Servers: ', value=serverCount, inline=True)
        #embed.add_field(name='Total Users: ', value=memberCount, inline=True)

        await ctx.send(embed=embed, view=view)


    @commands.command(aliases=['close', 'exit', 'stop'])
    @commands.is_owner()
    async def logout(self, ctx):
        # Shutdown the bot, only usable by the owner.
        await ctx.send(f'Logging out by {ctx.author.mention}\'s request. :wave:')
        await self.client.close()


    @commands.command(name='whois', aliases=['invite', 'invites'])
    async def whois(self, ctx, arg):
        # Lookup command to find out who invited who!
        # Type !whois (user_id) to find out who invited them to the server!
        try:
            member = IF.get_invite(arg)
            inviter = member['inviter_name']
            invitee = member['invitee_name']
            time = member['time']

            embed = discord.Embed(title=f'{invitee} was invited by {inviter}',
                                description='', colour=discord.Colour(0xd9a064))
            embed.set_thumbnail(url=self.logo)
            embed.add_field(
                name=f'Joined {time}', value='\uFEFF', inline=True)
            await ctx.send(embed=embed)
        except:
            print("ERROR: Could not find user [whois] in OnCommands")
            embed = discord.Embed(  title=f'Sorry, I could not find that user.',
                                    description='Try: !whois user_id',
                                    colour=discord.Colour(0xd9a064))
            embed.set_thumbnail(url=self.logo)
            await ctx.send(embed=embed)


async def setup(client):
  await client.add_cog(OnCommands(client))