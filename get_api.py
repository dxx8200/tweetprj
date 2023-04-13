import tweepy
import json
import os

DEFAULT_TKPATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'../config/tc.json'))

def OAuth1(tk_path = DEFAULT_TKPATH):
    consumer_key, consumer_secret, access_key, access_secret = from_file(tk_path)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def OAuth2(tk_path = DEFAULT_TKPATH):
    consumer_key, consumer_secret, _, _ = from_file(tk_path)
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def from_file(file_name):
    with open(file_name) as cred_data:
        info = json.load(cred_data)    
        return info['CONSUMER_KEY'],info['CONSUMER_SECRET'],info['ACCESS_KEY'],info['ACCESS_SECRET']

