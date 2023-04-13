from get_api import OAuth1
import tweepy
import shutil
import timeline
import user
import media
import download
import time
import os
import datetime
from json import JSONEncoder
import dateutil.parser
from html_util import htmlParser
from chat import Chat

MEDIA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../media'))
L0_PATH = os.path.join(MEDIA_PATH, 'L0')
L1_PATH = os.path.join(MEDIA_PATH, 'L1')
L2_PATH = os.path.join(MEDIA_PATH, 'L2')
BL_PATH = os.path.join(MEDIA_PATH, 'block')
DEL_PATH = os.path.join(MEDIA_PATH, 'delete')
BL_FILE = os.path.join(MEDIA_PATH, "block.txt")
NEW_PATH = os.path.join(MEDIA_PATH, 'new')

HTML_FOLDER = '_html'
HTML_PATH = '.html'
LOAD_TIME_INTERVAL = 60*60*24*2 # 2 Days
LOAD_L1_INTERVAL = 60*60*24*5 # 5 Days
MESSAGE_INTERVAL = 60*60*0.5 # 0.5 Hour
MAX_NEW_USERS = 500

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

# custom Decoder
def DecodeDateTime(empDict):
   if 'created_at' in empDict:
      empDict["created_at"] = dateutil.parser.parse(empDict["created_at"])
      return empDict

def download_media(tweets, uname, download_path):
    list_url = []
    for tweet in tweets:
        if tweet and tweet['media']:
            list_url.extend(tweet['media'])
    list_download = [file[1] for file in list_url if not os.path.exists(os.path.join(download_path,os.path.basename(file[1]).split('?')[0]))]
    len_download = len(list_download)
    for i in range(len_download):
        file = list_download[i]
        print(f'Downloading[{uname}][{i+1}/{len_download}][{file}]')
        download.download_file(file, download_path)
    return list_download

def get_list_from_file(path):
    with open(path, 'r') as f:
        return f.read().split('\n')
    
def get_related_users(api, tweets, user_screen_name):
    #mentioned_users = user.mentioned_users(all_tweets)
    #reply_users = user.reply_users(all_tweets)
    return user.get_friends(api, user_screen_name) #+ user.mentioned_users(tweets)

def load_user_list(src_path):
    return sorted([d.name for d in os.scandir(src_path) if d.is_dir() and not d.name==HTML_FOLDER], key=str.lower)

def download_tweets(api, tweets, user_screen_name):
    new_raw_tweets = []
    if tweets:
        new_raw_tweets = timeline.get_all_tweets(api, screen_name=user_screen_name, since_id=tweets[0].get('id'))
    else:
        new_raw_tweets = timeline.get_all_tweets(api, screen_name=user_screen_name)
    return new_raw_tweets

def load_user_tweets(api, user_screen_name, tweet_folder, current_level):
    tweet_html_file = os.path.join(tweet_folder, '../'+current_level+HTML_FOLDER, user_screen_name+HTML_PATH)
    tweet_html = htmlParser(user_screen_name, tweet_html_file, current_level)
    new_tweets = download_tweets(api, tweet_html.get_tweets(), user_screen_name)
    new_medias = media.get_all_media(new_tweets)
    tweet_html.update_tweets(new_tweets, new_medias) 
    tweet_html.save()   
    return new_tweets, download_media(tweet_html.get_tweets(), user_screen_name, os.path.join(tweet_folder, user_screen_name)) 

##########################################################################
# Main Function
##########################################################################
def main(api, chat):
    last_load_time = 0 # the last time load from hard drvie
    last_message_time = 0 # the last time send a message
    #last_l1_load_time = 0 

    l0_list = []
    l1_list = []
    l2_list = []
    block_list = []
    
    has_updated = 0
    dict_user_path = {}
    current_level = 'l0'
    current_list = []
    #l1_loaded = False
    #
    # Main Loop
    while True:
        current_time = time.time()
        if (current_time - last_load_time > LOAD_TIME_INTERVAL) or (len(current_list) <= 0 and current_level == 'new'):
            last_load_time = time.time()
            l0_list = load_user_list(L0_PATH)
            l1_list = load_user_list(L1_PATH)
            l2_list = load_user_list(L2_PATH)
            new_list = load_user_list(NEW_PATH)
            block_list = get_list_from_file(BL_FILE)  #load_user_list(BL_PATH)
            
            has_updated = 0
            
            dict_user_path.clear()
            dict_user_path.update({d:L0_PATH for d in l0_list})
            dict_user_path.update({d:L1_PATH for d in l1_list})
            dict_user_path.update({d:L2_PATH for d in l2_list})
            dict_user_path.update({d:NEW_PATH for d in new_list})
            
            current_level = 'l0'
            current_list = l0_list
            
            chat.send(f"=== Lists L0[{len(l0_list)}] L1[{len(l1_list)}] L2[{len(l2_list)}] New[{len(new_list)}] block[{len(block_list)}] ===")
            
        elif len(current_list) <= 0:
            if current_level == 'l0':
                current_list = l1_list
                current_level = 'l1'
            elif current_level == 'l1':
                current_list = l2_list
                current_level = 'l2'
            elif current_level == 'l2':
                current_list = new_list
                current_level = 'new'
                
        # Update the wait list
        current_user = ""
        try:
            current_user = current_list.pop(0)
            if current_user in block_list:
                continue 
            
            # get new tweets       
            new_tweets, list_download = load_user_tweets(api, current_user, dict_user_path[current_user], current_level)
            if len(list_download) > 0:
                has_updated = has_updated + 1
            
            # get related users for l0
            if current_user in l0_list:
                related_users = set(get_related_users(api, new_tweets, current_user))
                new_users = [u for u in related_users if u not in dict_user_path.keys() and u not in block_list]
                if len(new_list) < MAX_NEW_USERS:
                    new_list.extend(new_users)
                    dict_user_path.update({d:NEW_PATH for d in new_users})
                if len(new_list) > MAX_NEW_USERS:
                    new_list = new_list[:MAX_NEW_USERS]
                           
            message = f'Processed[{current_user}] new[{len(list_download)}] current_list_len[{len(current_list)}] current_level[{current_level}]'
            print(message)
            #chat.send(message)
            
            if current_time - last_message_time > MESSAGE_INTERVAL:
                chat.send(f"=== Current_list[{len(current_list)}] Current_Level[{current_level}] Updated[{has_updated}] New[{len(new_list)}] Current[{current_user}] ===")
                last_message_time = current_time
                
        except tweepy.error.TweepError as err:
            if err.api_code == 34:
                try:
                    shutil.move(os.path.join(dict_user_path[current_user], current_user), os.path.join(DEL_PATH, current_user))   
                    del dict_user_path[current_user]
                except:
                    pass
            if err.api_code == None and err.reason == 'Not authorized.':
                try:
                    shutil.move(os.path.join(dict_user_path[current_user], current_user), os.path.join(DEL_PATH, current_user))   
                    del dict_user_path[current_user]
                except:
                    pass
            message = f'User[{current_user}] Error[{str(err)}]'
            print(message)
            chat.send(message)   
        except Exception as e:
            message = f'User[{current_user}] Error[{str(e)}]'
            print(message)
            chat.send(message)

           
if __name__ == "__main__":
    main(OAuth1(), Chat())

