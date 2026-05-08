import pandas as pd
from sklearn.model_selection import train_test_split
from app.services.market_service import get_historical_data
from app.utils.indicators import calculate_indicators, prepare_features, create_labels
from app.ml.random_forest import train_rf
from app.ml.xgboost_model import train_xgb

ASSETS_TO_TRAIN = ["BTC", "ETH", "OR", "PETROLE"]


def train_all_models():
    all_X = []
    all_y = []

    for asset in ASSETS_TO_TRAIN:
        print(f"Téléchargement données {asset}...")
        df = get_historical_data(asset, period="2y")
        if df is None or df.empty:
            print(f"Pas de données pour {asset}")
            continue

        df = calculate_indicators(df)
        labels = create_labels(df)
        features = prepare_features(df)

        labels = labels[features.index]
        all_X.append(features)
        all_y.append(labels)
        print(f"{asset} — {len(features)} lignes ✅")

    if not all_X:
        print("Aucune donnée disponible")
        return

    X = pd.concat(all_X)
    y = pd.concat(all_y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Entraînement sur {len(X_train)} lignes...")
    train_rf(X_train, y_train)
    train_xgb(X_train, y_train)
    print("Entraînement terminé ! 🚀")


if __name__ == "__main__":
    train_all_models()