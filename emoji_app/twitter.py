import json
import os

import emoji as emoji_lib
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from emoji_app import config


all_emoji_unicode = emoji_lib.UNICODE_EMOJI.keys()

# Without special API access, can only filter by 400 emojis at a time
emojis_to_track = all_emoji_unicode[:config.MAX_EMOJIS_TO_QUERY]


class EmojiListener(StreamListener):

    def __init__(self, emoji_aggregator=None):
        self.emoji_aggregator = emoji_aggregator
        super(EmojiListener, self).__init__()

    def increment_emoji(self, emoji_name):
        if self.emoji_aggregator:
            self.emoji_aggregator.add_emoji(emoji_name)

    def on_data(self, data):
        text = json.loads(data).get("text")
        if not text:
            return True
        words = text.split()
        for word in words:
            emoji_name = emoji_lib.UNICODE_EMOJI.get(word)
            if emoji_name:
                self.increment_emoji(emoji_name)
        return True

    def on_error(self, status):
        print status


def start_stream(emoji_aggregator=None):
    listener = EmojiListener(emoji_aggregator)
    auth = OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

    # TODO: don't do this... use a secure library
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()

    stream = Stream(auth, listener)
    stream.filter(track=emojis_to_track)
