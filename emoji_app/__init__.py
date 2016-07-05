import os
import redis

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import config as cfg


app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app)
config = cfg.get_config()
redis_conn = redis.StrictRedis(**config.REDIS_SERVER)

Bootstrap(app)
