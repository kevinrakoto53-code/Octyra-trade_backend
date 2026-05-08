# app/core/warmup.py
import time
from app.services.market_service import get_all_prices, get_candles, ASSETS
from app.services.ml_service import get_all_signals

def warmup_cache():
    print("🔥 Chargement des prix...")
    try:
        get_all_prices()
    except Exception as e:
        print(f"Prix ignorés: {e}")

    print("🔥 Chargement des candles...")
    for asset in ASSETS.keys():
        try:
            get_candles(asset, period="5d", interval="1h")
            time.sleep(0.5)  # ✅ évite le blocage Yahoo
        except Exception as e:
            print(f"Candle {asset} ignoré: {e}")

    print("🔥 Chargement des signaux...")
    try:
        get_all_signals()
    except Exception as e:
        print(f"Signaux ignorés: {e}")

    print("Cache prêt ✅")