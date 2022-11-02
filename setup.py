def get_token():
    with open('key.key', 'r') as f:
        file_lines = f.readlines()
        for line in file_lines:
            bot_token = line.strip()
    return bot_token
