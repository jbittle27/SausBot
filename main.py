import lightbulb
import hikari
from hikari import intents
import random
import os
from setup import get_token

# global variables
cwd = os.getcwd()
bot_token = get_token()

# bot initialization
bot = lightbulb.BotApp(
    token=bot_token,
    intents=hikari.Intents.ALL,
    default_enabled_guilds=()  # for future / commands
)


def initialize_invite_created(event):
    user_directory = f'{cwd}\\servers\\{event.guild_id}\\invite_users\\{event.invite.inviter.username}'
    user_invited_file = f'{cwd}\\servers\\{event.guild_id}\\invite_users\\{event.invite.inviter.username}\\{event.invite.inviter.username}.txt'
    user_codes_file = f'{cwd}\\servers\\{event.guild_id}\\invite_users\\{event.invite.inviter.username}\\{event.invite.inviter.username}_codes.txt'
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    with open(user_codes_file, 'a') as f:
        f.write(
            f'{event.code}|{event.invite.uses}|{event.invite.max_uses}|{event.invite.expires_at}')
    with open(user_invited_file, 'a') as f:
        pass


def parse_invite(event):
    pass


def compare_invite_uses(event):
    pass


# On user join
@bot.listen(hikari.MemberCreateEvent)
async def member_joined(event):
    # TODO parse current invite
    # update invite uses for all codes (yikes)
    # check updated invite records with old invited records
    # record member joined under proper inviter
    pass


# On user creating invite
@bot.listen(hikari.InviteCreateEvent)
async def created_invite(event):
    initialize_invite_created(event)
    print('hit hikari')


bot.run()
