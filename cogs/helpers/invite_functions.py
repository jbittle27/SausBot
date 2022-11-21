import json
import os
import discord
import DiscordUtils
import datetime

script_dir = os.path.dirname(__file__)
rel_path = 'data\invite_data.json'
abs_file_path = os.path.join(script_dir, rel_path)

def remove_empty_elements(d):
    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}

def add_invite(new_user):
  with open(abs_file_path, 'r+') as file:
      file_data = json.load(file)
      file_data["Members"].append(new_user)
      file.seek(0)
      json.dump(file_data, file, indent = 4)
  

def remove_invite(userid):
  with open(abs_file_path, 'r+') as file:
    file_data = json.load(file)
    for idx, obj in enumerate(file_data["Members"]):
      if userid in obj.keys():
        del obj[userid]
        break
  file_data = remove_empty_elements(file_data)
  with open(abs_file_path, 'w') as file:
    json.dump(file_data, file, indent=4)

def get_invite(userid):
  with open(abs_file_path, 'r') as file:
    file_data = json.load(file)
    file_data = file_data["Members"]
    for person in file_data:
      if f'{userid}' in person.keys():
        return person[f"{userid}"]
  