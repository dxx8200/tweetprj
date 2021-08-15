import tweepy

def get_all(api, hashtag):
    for tweet in tweepy.Cursor(api.search, q='#' + hashtag, rpp=100).items(max_num):
        with open('hashtag_' + hashtag + '.txt', 'a') as the_file:
            the_file.write(str(tweet.text.encode('utf-8')) + '\n')

    print ('Extracted ' + str(max_num) + ' tweets with hashtag #' + hashtag)

def get_all_hastags(all_tweets):
    res = set()
    for status in all_tweets:
        if hasattr(status, 'entities'):
            if hasattr(status.entities, 'hashtags'):
                hashtags = status.entities.get('hashtags', [])
                for hashtag in hashtags:
                    res.add(hashtag.text)  
    return res      
