import datetime
import json

from emoji_app import redis_conn


STATS_LATEST_DELTA_REDIS_KEY = "stats_latest_delta"


def precompute_latest_delta(emoji, latest_value=None):
    """
    Compute and store the delta between current "price" and
    the price one day ago
    """
    from emoji_app.models import StockHistory

    histories = emoji.stock_histories

    if not latest_value:
        latest_value = emoji.latest_stock_price.value

    time_now = datetime.datetime.utcnow()
    yesterday = time_now - datetime.timedelta(days=1)

    # Might also want to filter here to make sure it's at least some distance away from
    # the current time. Otherwise the delta won't really reflect a day-to-day change
    yesterday_stock = histories.filter(StockHistory.date >= yesterday).first()
    yesterday_value = yesterday_stock.value if yesterday_stock else 0

    delta = latest_value - yesterday_value
    percent_change = "{0:.2f}".format((delta / float(yesterday_value)) * 100) if yesterday_value != 0 else None

    value_to_store = {
        "delta": delta,
        "percent_change": percent_change
    }

    redis_conn.hset(STATS_LATEST_DELTA_REDIS_KEY, emoji.name, json.dumps(value_to_store))
    return delta, percent_change


def get_stats_for_emoji(emoji):
    """
    Return a stats dict for the emoji over the last day
    """
    stats = redis_conn.hget(STATS_LATEST_DELTA_REDIS_KEY, emoji.name)
    if stats:
        return json.loads(stats)
    else:
        delta, percent_change = precompute_latest_delta(emoji)
        return {
            "delta": delta,
            "percent_change": percent_change
        }
