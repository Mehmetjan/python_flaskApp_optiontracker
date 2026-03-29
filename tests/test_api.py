import pytest
import requests

BASE = "http://127.0.0.1:5000"

# ── Health Check ─────────────────────────────────────────────
def test_health_check():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

# ── Home ─────────────────────────────────────────────────────
def test_home_returns_app_info():
    r = requests.get(f"{BASE}/")
    assert r.status_code == 200
    assert "app" in r.json()
    assert r.json()["app"] == "OptionsTrackr"

# ── POST /stocks ─────────────────────────────────────────────
def test_add_valid_ticker():
    r = requests.post(f"{BASE}/stocks", json={"ticker": "AAPL"})
    assert r.status_code == 201
    data = r.json()
    assert data["ticker"] == "AAPL"
    assert data["price"] > 0
    assert "timestamp" in data

def test_add_ticker_missing_body():
    r = requests.post(f"{BASE}/stocks", json={})
    assert r.status_code == 400
    assert "error" in r.json()

def test_add_invalid_ticker():
    r = requests.post(f"{BASE}/stocks", json={"ticker": "FAKEXYZ123"})
    assert r.status_code in [404, 500]
    assert "error" in r.json()

# ── GET /stocks ───────────────────────────────────────────────
def test_get_all_stocks_returns_list():
    r = requests.get(f"{BASE}/stocks")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_all_stocks_has_required_fields():
    r = requests.get(f"{BASE}/stocks")
    stocks = r.json()
    if len(stocks) > 0:
        stock = stocks[0]
        assert "ticker"    in stock
        assert "price"     in stock
        assert "volume"    in stock
        assert "timestamp" in stock

# ── GET /stocks/<ticker> ──────────────────────────────────────
def test_get_existing_ticker():
    # First add it
    requests.post(f"{BASE}/stocks", json={"ticker": "SPY"})
    # Then fetch it
    r = requests.get(f"{BASE}/stocks/SPY")
    assert r.status_code == 200
    assert r.json()["ticker"] == "SPY"

def test_get_nonexistent_ticker():
    r = requests.get(f"{BASE}/stocks/FAKEXYZ123")
    assert r.status_code == 404
    assert "error" in r.json()

def test_ticker_case_insensitive():
    requests.post(f"{BASE}/stocks", json={"ticker": "QQQ"})
    r = requests.get(f"{BASE}/stocks/qqq")   # lowercase
    assert r.status_code == 200
    assert r.json()["ticker"] == "QQQ"

# ── DELETE /stocks/<ticker> ───────────────────────────────────
def test_delete_existing_ticker():
    requests.post(f"{BASE}/stocks", json={"ticker": "TSLA"})
    r = requests.delete(f"{BASE}/stocks/TSLA")
    assert r.status_code == 200
    assert "deleted" in r.json()["message"]

def test_delete_nonexistent_ticker():
    r = requests.delete(f"{BASE}/stocks/FAKEXYZ123")
    assert r.status_code == 404