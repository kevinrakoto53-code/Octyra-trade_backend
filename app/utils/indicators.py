import pandas as pd


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    df["bb_middle"] = df["Close"].rolling(20).mean()
    std = df["Close"].rolling(20).std()
    df["bb_upper"] = df["bb_middle"] + 2 * std
    df["bb_lower"] = df["bb_middle"] - 2 * std

    df["returns"] = df["Close"].pct_change()
    df["volume_ma"] = df["Volume"].rolling(20).mean()

    df.dropna(inplace=True)
    return df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    feature_cols = [
        "rsi", "macd", "macd_signal", "macd_hist",
        "bb_upper", "bb_middle", "bb_lower",
        "returns", "volume_ma", "Close", "Volume",
    ]
    return df[feature_cols]


def create_labels(df: pd.DataFrame, threshold: float = 0.001) -> pd.Series:
    future_returns = df["Close"].shift(-1) / df["Close"] - 1
    labels = pd.Series("HOLD", index=df.index)
    labels[future_returns > threshold] = "BUY"
    labels[future_returns < -threshold] = "SELL"
    return labels