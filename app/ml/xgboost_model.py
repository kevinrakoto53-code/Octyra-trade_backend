import joblib
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import os

MODEL_PATH = "app/ml/saved_models/xgboost.pkl"
ENCODER_PATH = "app/ml/saved_models/xgb_encoder.pkl"


def train_xgb(X_train, y_train):
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_train)

    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="mlogloss",
        verbosity=0
    )
    model.fit(X_train, y_encoded)

    os.makedirs("app/ml/saved_models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print("XGBoost sauvegardé ✅")
    return model, le


def predict_xgb(X) -> str:
    if not os.path.exists(MODEL_PATH):
        return "HOLD"
    model = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)
    prediction = model.predict([X])[0]
    return le.inverse_transform([prediction])[0]


def load_xgb():
    if not os.path.exists(MODEL_PATH):
        return None, None
    return joblib.load(MODEL_PATH), joblib.load(ENCODER_PATH)