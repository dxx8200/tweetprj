import tweepy

def get_user(api, user_id=''):
    return api.get_user(user_id)

def get_friends(api, user_id=''):
    #return [friend.screen_name for friend in tweepy.Cursor(api.friends, 
    #id=user_id, skip_status=True, include_user_entities=False).items()]
    try:
        return [friend.screen_name for friend in api.friends(id=user_id, skip_status=True, include_user_entities=False)]
    except tweepy.error.TweepError as err:
        print("Tweepy Error:{0}".format(err))
        return []

def get_followers(api, user_id=''):
    try:
        return [follower.screen_name for follower in api.followers(id=user_id, skip_status=True, include_user_entities=False)]
    except tweepy.error.TweepError as err:
        print("Tweepy Error:{0}".format(err))
        return []

def reply_users(all_tweets):
    res = set()
    for status in all_tweets:
        if hasattr(status, 'in_reply_to_screen_name'):
            if status.in_reply_to_screen_name is not None:
                res.add(status.in_reply_to_screen_name)
    return list(res)

def mentioned_users(all_tweets):
    res = set()
    for status in all_tweets:
        if hasattr(status, 'entities'):
            for user in status.entities.get('user_mentions', []):
                if 'screen_name' in user:
                    res.add(user['screen_name'])
    return list(res)