# app/core/yfinance_patch.py
import yfinance as yf
import requests

def patch_yfinance():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    })
    yf.set_tz_cache_location("cache/")