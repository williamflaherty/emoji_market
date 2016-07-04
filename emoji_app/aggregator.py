from emoji_app import models
from emoji_app import redis_conn


class EmojiAggregator():
    """
    n.b. This is janky af

    Grab all of the redis key/values and create the appropriate models to store in the db
    Then, flush redis LOL
    """
    def run(self):
        emoji_counts = {name: redis_conn.get(name) for name in redis_conn.keys()}
        redis_conn.flushall()

        count = 0
        emojis = models.Emoji.query.all()
        for emoji in emojis:
            number_seen = int(emoji_counts.get(emoji.name, 0))
            if emoji.name in emoji_counts:
                del emoji_counts[emoji.name]
            emoji.add_stock_history(number_seen)

            count += number_seen

        # Add any new emojis
        for new_emoji in emoji_counts.keys():
            emoji = models.Emoji.create(name=new_emoji)
            number_seen = int(emoji_counts[new_emoji])
            emoji.add_stock_history(number_seen)

            count += number_seen

        return count