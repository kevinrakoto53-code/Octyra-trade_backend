import json
import pandas as pd
import yfinance as yf
from app.core.redis import cache_get, cache_set

ASSETS = {
    "BTC":     "BTC-USD",
    "EUR":     "EURUSD=X",
    "ETH":     "ETH-USD",
    "OR":      "GLD",      
    "DOGE":    "DOGE-USD",
    "PETROLE": "USO",       
    "SOL":     "SOL-USD",
    "BNB":     "BNB-USD",
    "GAZ":     "UNG",        
    "JPY":     "JPY=X",      
    "XRP":     "XRP-USD",
    "ADA":     "ADA-USD",
    "AVAX":    "AVAX-USD",
    "ARGENT":  "SLV",       
    "GBP":     "GBPUSD=X",
    "CHF":     "CHFUSD=X",
    "AUD":     "AUDUSD=X",
    "CAD":     "CADUSD=X",
}


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def get_price(asset: str) -> dict:
    cache_key = f"price:{asset}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    symbol = ASSETS.get(asset.upper())
    if not symbol:
        return {"error": f"Asset {asset} non supporté"}

    try:
        ticker = yf.Ticker(symbol)
        fast = ticker.fast_info
        info = ticker.info

        last_price = fast.last_price
        previous_close = fast.previous_close

        if last_price is None or previous_close is None:
            raise ValueError("Prix None")

        data = {
            "asset": asset.upper(),
            "name": info.get("longName") or info.get("shortName", asset),
            "price": round(float(last_price), 4),
            "change_24h": round(
                float(last_price - previous_close) / float(previous_close) * 100, 2
            ),
            "currency": "USD",
            "market_cap": info.get("marketCap", None),
            "circulating_supply": info.get("circulatingSupply", None),
            "volume_24h": (
                info.get("volume24Hr") or
                info.get("regularMarketVolume", None)
            ),
            "high_24h": info.get("dayHigh", None),
            "low_24h": info.get("dayLow", None),
        }

        cache_set(cache_key, json.dumps(data), expire=30)
        return data

    except Exception:
        try:
            df = yf.download(symbol, period="1d", interval="1m", progress=False)
            df = _flatten_columns(df)
            if not df.empty:
                last = float(df["Close"].iloc[-1])
                data = {
                    "asset": asset.upper(),
                    "name": asset.upper(),
                    "price": round(last, 4),
                    "change_24h": 0.0,
                    "currency": "USD",
                    "market_cap": None,
                    "circulating_supply": None,
                    "volume_24h": None,
                    "high_24h": None,
                    "low_24h": None,
                }
                cache_set(cache_key, json.dumps(data), expire=30)
                return data
        except Exception:
            pass
        return {"error": f"Prix indisponible pour {asset}"}


def get_all_prices() -> list:
    return [get_price(asset) for asset in ASSETS.keys()]


def get_candles(asset: str, period: str = "5d", interval: str = "1h") -> list:
    cache_key = f"candles:{asset}:{period}:{interval}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    symbol = ASSETS.get(asset.upper())
    if not symbol:
        return []

    df = yf.download(symbol, period=period, interval=interval, progress=False)
    if df is None or df.empty:
        return []

    df = _flatten_columns(df)

    candles = []
    for timestamp, row in df.iterrows():
        try:
            candles.append({
                "timestamp": int(timestamp.timestamp() * 1000),
                "open":   round(float(row["Open"]),   4),
                "high":   round(float(row["High"]),   4),
                "low":    round(float(row["Low"]),    4),
                "close":  round(float(row["Close"]),  4),
                "volume": round(float(row["Volume"]), 2),
            })
        except (TypeError, ValueError) as e:
            print(f"Bougie ignorée ({timestamp}): {e}")
            continue

    cache_set(cache_key, json.dumps(candles), expire=300)
    return candles


def get_historical_data(asset: str, period: str = "2y"):
    symbol = ASSETS.get(asset.upper())
    if not symbol:
        return None

    df = yf.download(symbol, period=period, progress=False)
    if df is None or df.empty:
        return None

    df = _flatten_columns(df)
    return df