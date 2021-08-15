import tweepy
import wget

def media_type(media):
    type = ''
    url = ''
    if 'type' in media:
       type = media['type']
    if type == 'photo':
        if 'media_url_https' in media:
            url = media['media_url_https']
    elif type == 'video' or type == 'animated_gif':
        if 'video_info' in media:
            if 'variants' in media['video_info']:
                variants = media['video_info']['variants']
                max_bitrate = 0
                for variant in variants:
                    if 'bitrate' in variant:
                        bitrate = variant['bitrate']
                        if bitrate >= max_bitrate and 'url' in variant:
                            url = variant['url']
                            max_bitrate = bitrate
        elif 'url' in media:
            url = media['url']

    return type, url

def get_all_media(all_tweets):
    media_types = ['photo', 'video', 'animated_gif']
    dict_res = {}
    for status in all_tweets:
        medias = []
        if hasattr(status, 'extended_entities'):
            medias = status.extended_entities.get('media', [])
        elif hasattr(status, 'entities'):
            medias = status.entities.get('media', [])

        for media in medias:
            type, url = media_type(media)
            if type in media_types:
                if status.id in dict_res:
                    dict_res[status.id].append((type,url))
                else:
                    dict_res[status.id] = [(type,url)]
        
    return dict_res
