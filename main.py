from get_api import OAuth1
import timeline
import search
import user
import media
import hashtag
import download
import time
import os
import json
import datetime
from datetime import timedelta
from json import JSONEncoder
import dateutil.parser
from html_util import htmlParser

MEDIA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../media'))
L0_PATH = os.path.join(MEDIA_PATH, 'L0')
L1_PATH = os.path.join(MEDIA_PATH, 'L1')
L2_PATH = os.path.join(MEDIA_PATH, 'L2')
BL_PATH = os.path.join(MEDIA_PATH, 'delete')
NEW_PATH = os.path.join(MEDIA_PATH, 'new')
HTML_PATH = '_.html'
ACCESS_INTERVAL = 2 # Seconds
LOAD_TIME_INTERVAL = 60*60*24*2 # 2 Days
LOAD_L1_INTERVAL = 60*60*24*5 # 5 Days
max_users = 2000

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

def download_media(tweets, download_path):
    list_url = []
    for tweet in tweets:
        if tweet and tweet['media']:
            list_url.extend(tweet['media'])
    list_download = [file[1] for file in list_url if not os.path.exists(os.path.join(download_path,os.path.basename(file[1]).split('?')[0]))]
    len_download = len(list_download)
    for i in range(len_download):
        file = list_download[i]
        print("downloading [%s] [%d/%d] [%s]...."%(download_path.split('\\')[-1],i+1,len_download,file))
        download.download_file(file, download_path)

def get_related_users(api, user_screen_name):
    #mentioned_users = user.mentioned_users(all_tweets)
    #reply_users = user.reply_users(all_tweets)
    return user.get_friends(api, user_screen_name)

def load_user_list(src_path):
    return sorted([d for d in os.listdir(src_path) if os.path.isdir(os.path.join(src_path,d))], key=str.lower)

def download_tweets(api, tweets, user_screen_name):
    new_raw_tweets = []
    if tweets:
        new_raw_tweets = timeline.get_all_tweets(api, screen_name=user_screen_name, since_id=tweets[0].get('id'))
    else:
        new_raw_tweets = timeline.get_all_tweets(api, screen_name=user_screen_name)
    return new_raw_tweets

def load_user_tweets(api, user_screen_name, tweet_folder):
    tweet_file = os.path.join(tweet_folder, HTML_PATH)
    tweet_html = htmlParser(tweet_file)
    new_tweets = download_tweets(api, tweet_html.get_tweets(), user_screen_name)
    new_medias = media.get_all_media(new_tweets)
    tweet_html.update_tweets(new_tweets, new_medias) 
    tweet_html.save()

    download_media(tweet_html.get_tweets(), tweet_folder)    
    return new_tweets

def main():
    api = OAuth1()
    last_load_time = last_access_time = last_l1_load_time = 0
    l0 = []; l1 = [];l2 = [];block = [];wait_list = [];has_update = [];has_accessed = []
    dict_user_path = {}
    l1_loaded = False
    while True:
        current_time = time.time()
        if current_time - last_load_time > LOAD_TIME_INTERVAL:
            last_load_time = time.time()
            l0 = load_user_list(L0_PATH)
            l1 = load_user_list(L1_PATH)
            l2 = load_user_list(L2_PATH)
            block = load_user_list(BL_PATH)
            has_update = []
            has_accessed = []
            dict_user_path.clear()
            dict_user_path.update({d:os.path.join(L0_PATH,d) for d in l0})
            dict_user_path.update({d:os.path.join(L1_PATH,d) for d in l1})
            dict_user_path.update({d:os.path.join(L2_PATH,d) for d in l2})
            wait_list.extend(l0)
        
        if current_time - last_l1_load_time > LOAD_L1_INTERVAL:
            l1_loaded = False

        if not l1_loaded and len(wait_list) == 0:
            wait_list.extend(l1)
            l1_loaded = True
            last_l1_load_time = time.time()

        current_user = wait_list.pop(0)
        if current_user in block:
            continue
        
        interval_time = current_time - last_access_time
        if interval_time < ACCESS_INTERVAL:
            time.sleep(ACCESS_INTERVAL - interval_time) 

        print(f'Processing user:[{current_user}]')
        has_accessed.append(current_user)
        last_access_time = time.time()
        if len(load_user_tweets(api, current_user, dict_user_path[current_user])) > 0:
            has_update.append(current_user)
            
        related_users = []
        if current_user in l0 or current_user in l1:
            related_users = set(get_related_users(api, current_user))
        related_users = [u for u in related_users if u not in l0 and u not in l1 and u not in l2 and u not in has_accessed]
        wait_list.extend(related_users)
        dict_user_path.update({d:os.path.join(NEW_PATH,d) for d in related_users})


if __name__ == "__main__":
    main()

