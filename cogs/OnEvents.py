from discord.ext import commands


class OnEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
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

    @commands.Cog.listener()
    async def on_ready(self):
        await client.change_presence(activity=discord.Game(name=f'Use ! to interact with me.'))

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
                await ctx.send(f'You must wait {int(n)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f'You must wait {int(h)} hours, {int(m)} minutes, and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry @{ctx.author.mention}, you lack the permission to use this command.')
        raise error

    @commands.Cog.listener()
    async def on_member_join(self, new_member):
        # When a member joins, save inviter, member, and time into db
        inviter = await tracker.fetch_inviter(new_member)
        invitedb.add_invite(f'{inviter}', f'{new_member}')
        return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # When a member leaves, remove invite information from db
        invitedb.remove_invite(member)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        # On Message Events
        # Ignore bot messages
        if message.author.id == client.user.id:
            return

        await client.process_commands(message)


async def setup(client):
    await client.add_cog(OnEvents(client))
