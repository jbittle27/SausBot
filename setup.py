def get_token():
    with open('key.key', 'r') as f:
        file_lines = f.readlines()
        for line in file_lines:
            bot_token = line.strip()
    return bot_token


def get_data():
    with open('data.txt', 'r') as f:
        channel_id = f.readline().strip()
        server_id = f.readline().strip()
    return channel_id, server_id
