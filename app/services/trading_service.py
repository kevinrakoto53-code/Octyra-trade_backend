import ccxt
from app.core.config import settings


def get_exchange():
    exchange = ccxt.binance({
        "apiKey": settings.BINANCE_API_KEY,
        "secret": settings.BINANCE_API_SECRET,
        "sandbox": True,  # Testnet !
        "enableRateLimit": True,
    })
    exchange.set_sandbox_mode(True)
    return exchange


ASSET_SYMBOLS = {
    "BTC": "BTC/USDT",
    "ETH": "ETH/USDT",
}


def execute_trade(asset: str, action: str, quantity: float = 0.001) -> dict:
    symbol = ASSET_SYMBOLS.get(asset.upper())
    if not symbol:
        return {"error": f"Asset {asset} non supporté pour le trading"}

    try:
        exchange = get_exchange()

        if action == "BUY":
            order = exchange.create_market_buy_order(symbol, quantity)
        elif action == "SELL":
            order = exchange.create_market_sell_order(symbol, quantity)
        else:
            return {"action": "HOLD", "executed": False}

        return {
            "action": action,
            "symbol": symbol,
            "quantity": quantity,
            "order_id": order.get("id"),
            "status": order.get("status"),
            "executed": True,
        }

    except Exception as e:
        return {
            "action": action,
            "executed": False,
            "error": str(e)
        }


def get_balance() -> dict:
    try:
        exchange = get_exchange()
        balance = exchange.fetch_balance()
        return {
            "USDT": balance.get("USDT", {}).get("free", 0),
            "BTC": balance.get("BTC", {}).get("free", 0),
            "ETH": balance.get("ETH", {}).get("free", 0),
        }
    except Exception as e:
        return {"error": str(e)}