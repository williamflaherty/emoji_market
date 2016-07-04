import os
import sys


def get_config():
    """
    Get the config class for the environment
    """
    app_settings_path = os.environ["APP_SETTINGS"]
    cls_name = app_settings_path.split(".")[-1]
    cls = getattr(sys.modules[__name__], cls_name)
    return cls


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
    TWITTER_SECRET = os.environ["TWITTER_SECRET"]
    TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
    TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    MAX_EMOJIS_TO_QUERY = None


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MAX_EMOJIS_TO_QUERY = 400

    REDIS_SERVER = {
        "host": "localhost",
        "port": 6379,
        "db": 0
    }


class TestingConfig(Config):
    TESTING = True
