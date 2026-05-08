# app/services/ml_service.py

import json
from app.services.market_service import get_historical_data, ASSETS
from app.utils.indicators import calculate_indicators, prepare_features
from app.ml.ensemble import ensemble_predict
from app.core.redis import cache_get, cache_set

def get_signal(asset: str) -> dict:
    cache_key = f"signal:{asset}"
    cached = cache_get(cache_key)
    if cached:
        return json.loads(cached)

    df = get_historical_data(asset, period="60d")
    if df is None or df.empty:
        return {"error": "Pas de données disponibles"}

    df = calculate_indicators(df)
    features = prepare_features(df)
    if features.empty:
        return {"error": "Pas assez de données"}

    last_row = features.iloc[-1].values.tolist()

    result = ensemble_predict(last_row)
    result["asset"] = asset.upper()
    cache_set(cache_key, json.dumps(result), expire=600)
    return result


def get_all_signals() -> list:
    return [get_signal(asset) for asset in ASSETS.keys()]