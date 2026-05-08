from datetime import datetime


def format_price(price: float, decimals: int = 2) -> str:
    return f"${price:,.{decimals}f}"


def format_percent(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def get_signal_color(signal: str) -> str:
    colors = {
        "BUY": "green",
        "SELL": "red",
        "HOLD": "orange"
    }
    return colors.get(signal.upper(), "gray")


def get_sentiment_emoji(sentiment: str) -> str:
    emojis = {
        "positive": "📈",
        "negative": "📉",
        "neutral":  "➡️"
    }
    return emojis.get(sentiment.lower(), "➡️")


def timestamp_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M")


def is_market_open() -> bool:
    now = datetime.utcnow()
    # Crypto toujours ouvert
    return True