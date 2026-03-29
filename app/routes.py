from flask import Blueprint, jsonify, request
from app.models import db, Stock
from app.fetcher import fetch_and_store

main = Blueprint("main", __name__)

@main.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "OptionsTrackr API is running"
    }), 200

@main.route("/", methods=["GET"])
def home():
    return jsonify({
        "app":       "OptionsTrackr",
        "version":   "1.0",
        "endpoints": ["/health", "/stocks"]
    }), 200

@main.route("/stocks", methods=["GET"])
def get_all_stocks():
    stocks = Stock.query.all()
    return jsonify([s.to_dict() for s in stocks]), 200

@main.route("/stocks/<ticker>", methods=["GET"])
def get_stock(ticker):
    stock = Stock.query.filter_by(
        ticker=ticker.upper()
    ).order_by(Stock.timestamp.desc()).first()

    if not stock:
        return jsonify({"error": f"{ticker} not found"}), 404

    return jsonify(stock.to_dict()), 200

@main.route("/stocks", methods=["POST"])
def add_stock():
    data   = request.get_json()
    ticker = data.get("ticker")

    if not ticker:
        return jsonify({"error": "ticker is required"}), 400

    result, status = fetch_and_store(ticker)
    return jsonify(result), status

@main.route("/stocks/<ticker>", methods=["DELETE"])
def delete_stock(ticker):
    stocks = Stock.query.filter_by(ticker=ticker.upper()).all()

    if not stocks:
        return jsonify({"error": f"{ticker} not found"}), 404

    for s in stocks:
        db.session.delete(s)
    db.session.commit()

    return jsonify({"message": f"{ticker} deleted"}), 200