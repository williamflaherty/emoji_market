import datetime

from emoji import db
from emoji_app.utils import AppModel


class Emoji(db.Model, AppModel):
    __tablename__ = "emoji"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<models.Emoji id=%s name="%s">' % (self.id, self.name)

    @property
    def stock_histories(self):
        return StockHistory.query.filter_by(emoji_id=self.id)

    @property
    def latest_stock_price(self):
        return StockHistory.query.order_by(
            StockHistory.date.desc()
        ).filter_by(emoji_id=self.id).first() 

    def add_stock_history(self, value):
        StockHistory.create(emoji_id=self.id, value=value)


class StockHistory(db.Model, AppModel):
    __tablename__ = "stockhistory"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    emoji_id = db.Column(db.Integer)
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<models.StockHistory id=%s emoji_id=%s>' % (self.id, self.emoji_id)

    @property
    def emoji(self):
        return Emoji.query.get(self.emoji_id)
