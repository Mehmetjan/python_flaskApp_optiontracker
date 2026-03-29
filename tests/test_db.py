import pytest
import requests

BASE = "http://127.0.0.1:5000"

def test_data_persists_after_add():
    """Add a stock then verify it exists in DB via API"""
    requests.post(f"{BASE}/stocks", json={"ticker": "MSFT"})
    r = requests.get(f"{BASE}/stocks/MSFT")
    assert r.status_code == 200
    assert r.json()["ticker"] == "MSFT"

def test_price_is_positive_number():
    requests.post(f"{BASE}/stocks", json={"ticker": "NVDA"})
    r = requests.get(f"{BASE}/stocks/NVDA")
    assert r.json()["price"] > 0

def test_volume_is_not_negative():
    requests.post(f"{BASE}/stocks", json={"ticker": "AAPL"})
    r = requests.get(f"{BASE}/stocks/AAPL")
    assert r.json()["volume"] >= 0

def test_timestamp_format():
    """Timestamp must be in YYYY-MM-DD HH:MM:SS format"""
    requests.post(f"{BASE}/stocks", json={"ticker": "SPY"})
    r = requests.get(f"{BASE}/stocks/SPY")
    ts = r.json()["timestamp"]
    from datetime import datetime
    try:
        datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        valid = True
    except ValueError:
        valid = False
    assert valid

def test_delete_removes_from_db():
    """After delete, ticker should return 404"""
    requests.post(f"{BASE}/stocks", json={"ticker": "AMD"})
    requests.delete(f"{BASE}/stocks/AMD")
    r = requests.get(f"{BASE}/stocks/AMD")
    assert r.status_code == 404