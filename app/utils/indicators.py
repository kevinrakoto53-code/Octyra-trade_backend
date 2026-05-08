import pandas as pd
import pandas_ta as ta


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # RSI — suracheté / survendu
    df["rsi"] = ta.rsi(df["Close"], length=14)

    # MACD — changement de tendance
    macd = ta.macd(df["Close"], fast=12, slow=26, signal=9)
    df["macd"] = macd["MACD_12_26_9"]
    df["macd_signal"] = macd["MACDs_12_26_9"]
    df["macd_hist"] = macd["MACDh_12_26_9"]

    # Bollinger Bands — zone normale du prix
    bbands = ta.bbands(df["Close"], length=20, std=2)
    df["bb_upper"] = bbands["BBU_20_2.0_2.0"]
    df["bb_middle"] = bbands["BBM_20_2.0_2.0"]
    df["bb_lower"] = bbands["BBL_20_2.0_2.0"]

    # Features supplémentaires
    df["returns"] = df["Close"].pct_change()
    df["volume_ma"] = ta.sma(df["Volume"], length=20)

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