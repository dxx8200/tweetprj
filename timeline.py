import tweepy
from get_api import from_file


def get_all_tweets(api, screen_name = '', count=999999, since_id = -1, max_id = -1):
    all_the_tweets = []
    left_count = count
    try:
        if left_count < 200:
            new_tweets = get_tweets(api, screen_name, left_count, since_id, max_id)
        else:
            new_tweets = get_tweets(api, screen_name, 200, since_id, max_id)
        while len(new_tweets) > 0:
            all_the_tweets.extend(new_tweets)
            left_count = left_count - len(new_tweets)
            if left_count <= 0:
                break
            if left_count < 200:
                new_tweets = get_tweets(api, screen_name, left_count, since_id, all_the_tweets[-1].id-1)
            else:   
                new_tweets = get_tweets(api, screen_name, 200, since_id, all_the_tweets[-1].id-1)
    except tweepy.error.TweepError as err:
        print("Tweepy Error:{0}".format(err))
    return all_the_tweets

def get_tweets(api, screen_name='', count = -1, since_id = -1, max_id = -1):
    if len(screen_name) <= 0:
        if count > 0:
            if max_id > 0:
                if since_id > 0:
                    return api.home_timeline(count = count, since_id = since_id, max_id = max_id)
                else:
                    return api.home_timeline(count = count, max_id = max_id)
            else:
                if since_id > 0:
                    return api.home_timeline(count = count, since_id = since_id)
                else:
                    return api.home_timeline(count = count)
        else:
            if max_id > 0:
                if since_id > 0:
                    return api.home_timeline(since_id = since_id, max_id = max_id)
                else:
                    return api.home_timeline(max_id = max_id)
            else:
                if since_id > 0:
                    return api.home_timeline(since_id = since_id)
                else:
                    return api.home_timeline()
    else:
        if count > 0:
            if max_id > 0:
                if since_id > 0:
                    return api.user_timeline(screen_name=screen_name, count = count, since_id = since_id, max_id = max_id)
                else:
                    return api.user_timeline(screen_name=screen_name, count = count, max_id = max_id)
            else:
                if since_id > 0:
                    return api.user_timeline(screen_name=screen_name, count = count, since_id = since_id)
                else:
                    return api.user_timeline(screen_name=screen_name, count = count)
        else:
            if max_id > 0:
                if since_id > 0:
                    return api.user_timeline(screen_name=screen_name, since_id = since_id, max_id = max_id)
                else:
                    return api.user_timeline(screen_name=screen_name, max_id = max_id)
            else:
                if since_id > 0:
                    return api.user_timeline(screen_name=screen_name, since_id = since_id)
                else:
                    return api.user_timeline(screen_name=screen_name)
