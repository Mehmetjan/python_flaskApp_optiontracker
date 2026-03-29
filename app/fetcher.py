import yfinance as yf
from app.models import db, Stock

def fetch_and_store(ticker):
    try:
        stock = yf.Ticker(ticker)
        info  = stock.fast_info

        price  = info.last_price
        volume = info.three_month_average_volume

        if not price:
            return {"error": f"No data found for {ticker}"}, 404

        # Save to MySQL
        record = Stock(
            ticker = ticker.upper(),
            price  = round(price, 2),
            volume = int(volume) if volume else 0
        )

        db.session.add(record)
        db.session.commit()

        return record.to_dict(), 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500