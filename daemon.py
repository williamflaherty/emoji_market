import threading

from emoji_app import twitter
from emoji_app.aggregator import EmojiAggregator


AGGREGATOR_SCHEDULE = 300  # 5 minutes


def _run_aggregator(emoji_aggregator):
    thread = threading.Timer(AGGREGATOR_SCHEDULE, _run_aggregator, [emoji_aggregator])
    thread.daemon = True
    thread.start()

    print "Running aggregator..."
    emoji_seen = emoji_aggregator.run()
    print "Detected %s emojis since last crawl" % (emoji_seen,)


def run_backend():
    emoji_aggregator = EmojiAggregator()
    _run_aggregator(emoji_aggregator)

    print "Starting twitter stream..."
    twitter.start_stream(emoji_aggregator)


if __name__ == "__main__":
    run_backend()
