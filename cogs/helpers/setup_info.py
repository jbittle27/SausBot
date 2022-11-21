import json
import os

script_dir = os.path.dirname(__file__)  # ABS pathname
rel_path = 'data\\setup_data.json'
abs_file_path = os.path.join(script_dir, rel_path)


def set_info():
    with open(f'{abs_file_path}', 'r') as file:
        data = json.load(file)
        for line in data['bot_info']:
            return (line)


def get_reaction_message_id():
    bot_info = set_info()
    return bot_info['reaction_message_id']


def get_verification_role():
    bot_info = set_info()
    return bot_info['verification_role']


def get_bot_owner_id():
    bot_info = set_info()
    return bot_info['bot_owner_id']


def get_rules_channel_id():
    bot_info = set_info()
    return bot_info['rules_channel_id']


def get_channel_id():
    bot_info = set_info()
    return bot_info['channel_id']


def get_token():
    bot_info = set_info()
    return bot_info['token']


def get_logo():
    bot_info = set_info()
    return bot_info['bot_logo']
