from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   # ← standalone instance, no circular import

class Stock(db.Model):
    __tablename__ = "stocks"

    id        = db.Column(db.Integer, primary_key=True)
    ticker    = db.Column(db.String(10), nullable=False)
    price     = db.Column(db.Float, nullable=False)
    volume    = db.Column(db.BigInteger)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":        self.id,
            "ticker":    self.ticker,
            "price":     self.price,
            "volume":    self.volume,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }