import json


def get_info():
    # Get general information for the bot.
    # Includes token & ids
    with open('setupinfo.json', 'r') as file:
        data = json.load(file)
        for line in data['bot_info']:
            return (line)


def set_info():
    bot_info = get_info()
    return bot_info['token'], bot_info['channel_id'], bot_info['server_id'], bot_info['rules_channel_id'], bot_info['bot_owner_id'], bot_info['reaction_message_id']
