import os
import redis

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import config as cfg


config = cfg.get_config()

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
redis_conn = redis.StrictRedis(**config.REDIS_SERVER)

Bootstrap(app)
