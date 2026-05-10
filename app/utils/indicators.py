import pandas as pd
import ta


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(df["Close"], window_fast=12, window_slow=26, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_middle"] = bb.bollinger_mavg()
    df["bb_lower"] = bb.bollinger_lband()

    # Features supplémentaires
    df["returns"] = df["Close"].pct_change()
    df["volume_ma"] = ta.trend.SMAIndicator(df["Volume"], window=20).sma_indicator()

    # Supprimer les lignes avec des valeurs manquantes
    df.dropna(inplace=True)

    return df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    feature_cols = [
        "rsi",
        "macd",
        "macd_signal",
        "macd_hist",
        "bb_upper",
        "bb_middle",
        "bb_lower",
        "returns",
        "volume_ma",
        "Close",
        "Volume",
    ]
    return df[feature_cols]


def create_labels(df: pd.DataFrame, threshold: float = 0.001) -> pd.Series:
    future_returns = df["Close"].shift(-1) / df["Close"] - 1

    labels = pd.Series("HOLD", index=df.index)
    labels[future_returns > threshold] = "BUY"
    labels[future_returns < -threshold] = "SELL"

    return labels