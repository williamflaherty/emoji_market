import json
import os

import emoji as emoji_lib
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from emoji_app import config
from emoji_app import redis_conn


all_emoji_unicode = emoji_lib.UNICODE_EMOJI.keys()

# Without special API access, can only filter by 400 emojis at a time
emojis_to_track = all_emoji_unicode[:config.MAX_EMOJIS_TO_QUERY]


class EmojiListener(StreamListener):

    def on_data(self, data):
        text = json.loads(data).get("text")
        if not text:
            return True
        for emoji_code in emojis_to_track:
            if emoji_code in text:
                name = emoji_lib.UNICODE_EMOJI[emoji_code]
                redis_conn.incr(name)
        return True

    def on_error(self, status):
        print status


def start_stream():
    listener = EmojiListener()
    auth = OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

    # TODO: don't do this... use a secure library
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()

    stream = Stream(auth, listener)
    stream.filter(track=emojis_to_track)
