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
import datetime



currentdir = os.path.dirname(os.path.abspath(
inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)


class OnEventReaction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reaction_message = SI.get_reaction_message_id()
        self.verification_role = SI.get_verification_role()
        self.logo = SI.get_logo()
        self.tracker = DiscordUtils.InviteTracker(self.client)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        guild_id = ctx.guild_id
        guild = discord.utils.find(
            lambda g: g.id == guild_id, self.client.guilds)
        role = discord.utils.get(guild.roles, name=self.verification_role)
        channel = self.client.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        user = self.client.get_user(ctx.user_id)
        user_emoji = ctx.emoji
        if self.reaction_message == ctx.message_id:
            if user_emoji.name == '✅':
                if role is not None:
                    member = discord.utils.find(
                        lambda m: m.id == ctx.user_id, guild.members)
                    if member is not None:
                        try:
                            await member.add_roles(role)
                            await message.remove_reaction('✅', user)
                        except:
                            print('ERROR: Could not add role to the user')
                            return
        else:
            try:
                member = discord.utils.find(
                    lambda m: m.id == ctx.user_id, guild.members)
                await message.remove_reaction(user_emoji, user)
                print(f'Removed unknown emoji from {member}')
            except:
                print('Error removing unknown emoji')
                return

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='Type !help to see my commands!'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
                await ctx.send(f'You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes, and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry @{ctx.author.mention}, you lack the permission to use this command.')
        raise error

    @commands.Cog.listener()
    async def on_member_join(self, invitee):
        inviter = await self.tracker.fetch_inviter(invitee)
        #f'{inviter}', inviter.id, f'{invitee}', invitee.id
        time = datetime.datetime.now()
        new_user = {
            f"{invitee.id}":{
            "invitee_name": f'{invitee}',
            "invitee_id": invitee.id,
            "inviter_name": f'{inviter}',
            "inviter_id": inviter.id,
            "time": time.strftime('%a, %b %d %Y at %I:%M %p')
            }
        }
        IF.add_invite(new_user)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            IF.remove_invite(f'{member.id}')
        except:
            print('ERROR: Could not remove user, check OnEventReaction')


async def setup(client):
    await client.add_cog(OnEventReaction(client))
