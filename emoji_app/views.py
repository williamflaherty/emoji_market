from flask import render_template

from emoji_app import app
from emoji_app import models


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/emojis/")
@app.route("/emojis/<name>")
def emojis(name=None):
    if name:
        emoji = models.Emoji.query.filter_by(name=name).first_or_404()
        return render_template("show_emoji.html", emoji=emoji)

    emojis = list(models.Emoji.query.all())
    sorted_emojis = sorted(emojis, key=lambda x: -x.latest_stock_price.value)
    return render_template("show_emojis.html", emojis=sorted_emojis)
