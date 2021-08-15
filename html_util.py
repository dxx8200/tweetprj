from html.parser import HTMLParser
import os
from datetime import datetime

class htmlParser(HTMLParser):
    def __init__(self, path):
        HTMLParser.__init__(self)
        self.tweets = []
        self.path = path
        self.is_parsing_tweet = False
        self.is_parsing_text = False
        self.new_tweet = {}
        self.parse(path)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.new_tweet["id"] = int(self.get_attr(attrs, "id"))
            self.new_tweet["created_at"] = datetime.strptime(self.get_attr(attrs, "created_at"),'%Y-%m-%d %H:%M:%S')
            self.new_tweet["source"] = self.get_attr(attrs, "source")
            self.new_tweet["source_url"] = self.get_attr(attrs, "soruce_url")
            self.new_tweet["lang"] = self.get_attr(attrs, "lang")
            self.new_tweet["retweet_count"] = self.get_attr(attrs, "retweet_count")
            self.new_tweet["media"] = []
            self.new_tweet["text"] = ""
            self.is_parsing_tweet = True
        
        if tag == 'p' and self.is_parsing_tweet:
            self.is_parsing_text = True

        if tag == 'img' and self.is_parsing_tweet:
            self.new_tweet["media"].append(('photo', self.get_attr(attrs, "src")))
        
        if tag == 'source' and self.is_parsing_tweet:
            self.new_tweet["media"].append(('video', self.get_attr(attrs, "src")))
            
    def get_attr(self, attrs, attr_str):
        for attr in attrs:
            if attr[0] == attr_str:
                return attr[1]
        return ""

    def handle_endtag(self, tag):
        if tag == 'div':
            self.is_parsing_tweet = False
            self.tweets.append(self.new_tweet)
            self.new_tweet = {}
        if tag == 'p':
            self.is_parsing_text = False

    def handle_data(self, data):
        if self.is_parsing_text:
            self.new_tweet["text"]=data

    def parse(self, path):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.feed(f.read())

    def update_tweets(self, new_raw_tweets, new_medias):
        new_tweets = []
        for tweet in new_raw_tweets:
            t_media = []
            if tweet.id in new_medias:
                t_media.extend(new_medias[tweet.id])
            new_tweets.append({
            'id':tweet.id,
            'text':tweet.text,
            'source':tweet.source,
            'source_url':tweet.source_url,
            'lang':tweet.lang,
            'retweet_count':tweet.retweet_count,
            'created_at':tweet.created_at,
            'media':t_media
            })
        new_tweets.extend(self.tweets)
        self.tweets = new_tweets
        
    def get_tweets(self):
        return self.tweets
    
    def gen_img(self, img_path):
        return f'\t<img src="{img_path}" width="300">'

    def gen_video(self, video_path):
        return f'\t<video width="300" controls><source src="{video_path}" type="video/mp4"></video>'
    
    def gen_text(self, text):
        return f'\t<p>{text}</p>'

    def gen_tweet(self, tweet):
        id = tweet["id"]
        created_at = tweet["created_at"]
        source = tweet["source"]
        source_url = tweet["source_url"]
        lang = tweet["lang"]
        retweet_count = tweet["retweet_count"]
        res = [f'<div id="{id}" created_at="{created_at}" source="{source}" source_url="{source_url}" lang="{lang}" retweet_count="{retweet_count}">']
        res.append(self.gen_text(tweet["text"]))
        if 'media' in tweet.keys():
            for m in tweet['media']:
                if m[0] == 'photo':
                    res.append(self.gen_img(m[1]))
                elif m[0] == 'video':
                    res.append(self.gen_video(m[1]))
        res.append('</div>')
        return '\n\t'.join(res)

    def gen_html_str(self):
        res = ['<!DOCTYPE html>',
               '<html>',
               '\t<head>',
               '\t\t<link rel="stylesheet" href="../style.css">',
               '\t</head>',
               '\t<body>']
        res.extend([self.gen_tweet(h) for h in self.tweets])
        res.append('\t</body>')
        res.append('</html>')
        return '\n'.join(res)

    def save(self):
        with open(self.path, 'w', encoding="utf-8") as f:
            f.write(self.gen_html_str())

#h = htmlParser('../media/b/a.html')
#h.save()


