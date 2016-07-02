from flask import Flask
from flask_bootstrap import Bootstrap

#@app.route('/')
#using application factories pattern wat
def create_app(configfile=None):
    app = Flask(__name__)
    Bootstrap( app )
    return app
