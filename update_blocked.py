import os
import json
from json import JSONEncoder
import datetime

media_path = "../media"
delete_path = "../media/delete"
src_blocked_users = "../blocked_users.json"

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

def load_blocked_users(src_path):
    blocked_users = []
    if os.path.exists(src_path):
        with open(src_path, 'r', encoding='utf8') as f:
            blocked_users = json.load(f)
    return blocked_users

def read_new_blocked(src_path):
    return os.listdir(src_path)

blocked_users = load_blocked_users(src_blocked_users)
blocked_users.extend(read_new_blocked(delete_path))

with open(src_blocked_users, 'w') as f:
    json.dump(sorted(set(blocked_users)), f, sort_keys=True, indent=4, cls=DateTimeEncoder, ensure_ascii=False)
