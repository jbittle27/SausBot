def get_token():
    with open('key.key', 'r') as f:
        file_lines = f.readlines()
        for line in file_lines:
            bot_token = line.strip()
    return bot_token


def get_data():
    with open('data.txt', 'r') as f:
        channel_id = f.readline().split(':')[1].strip()
        server_id = f.readline().split(':')[1].strip()
        rules_id = f.readline().split(':')[1].strip()
        owner_id = f.readline().split(':')[1].strip()
    channel_id = int(channel_id)
    server_id = int(server_id)
    rules_id = int(rules_id)
    owner_id = int(owner_id)
    return channel_id, server_id, rules_id, owner_id
