import tweepy
import csv
import json
import wget

# load Twitter API credentials

with open('tc.json') as cred_data:
    info = json.load(cred_data)
    
consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']
max_num = 500

def get_all_tweets(screen_name):
    # Twitter allows access to only 3240 tweets via this method
    # Authorization and initialization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialization of a list to hold all Tweets
    all_the_tweets = []

    # We will get the tweets with multiple requests of 200 tweets each
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # saving the most recent tweets
    all_the_tweets.extend(new_tweets)

    # save id of 1 less than the oldest tweet
    oldest_tweet = all_the_tweets[-1].id - 1

    # grabbing tweets till none are left
    while len(new_tweets) > 0:
        # The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest_tweet)
        # save most recent tweets
        all_the_tweets.extend(new_tweets)
        # id is updated to oldest tweet - 1 to keep track
        oldest_tweet = all_the_tweets[-1].id - 1
        print ('...%s tweets have been downloaded so far' % len(all_the_tweets))

    image_files = set()
    for status in all_the_tweets:
        media = status.entities.get('media', [])
        if len(media) > 0:
            image_files.add(media[0]['media_url'])

    print ('Downloading ' + str(len(image_files)) + ' images.....')
    for image_file in image_files:
        wget.download(image_file)

    # transforming the tweets into a 2D array that will be used to populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in all_the_tweets]

    # writing to the csv file
    with open(screen_name + '_tweets.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(outtweets)


def get_all_hashtag(hashtag):
    # Twitter allows access to only 3240 tweets via this method
    # Authorization and initialization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialization of a list to hold all Tweets
    all_the_tweets = []
    for tweet in tweepy.Cursor(api.search, q='#' + hashtag, rpp=100).items(max_num):
        with open('hashtag_' + hashtag + '.txt', 'a') as the_file:
            the_file.write(str(tweet.text.encode('utf-8')) + '\n')

    print ('Extracted ' + str(max_num) + ' tweets with hashtag #' + hashtag)

if __name__ == '__main__':
    # Enter the twitter handle of the person concerned
    get_all_tweets(input("Enter the twitter handle of the person whose tweets you want to download:- "))