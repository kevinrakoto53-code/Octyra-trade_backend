# app/ml/random_forest.py
import joblib
import numpy as np
import pandas as pd
import os

MODEL_PATH = "app/ml/saved_models/random_forest.pkl"
ENCODER_PATH = "app/ml/saved_models/rf_encoder.pkl"

def train_rf(X_train, y_train):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    y_encoded = le.fit_transform(y_train)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_encoded)  # ← X_train doit être un DataFrame ici

    os.makedirs("app/ml/saved_models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print("RandomForest sauvegardé ✅")
    return model, le

def predict_rf(X) -> str:
    if not os.path.exists(MODEL_PATH):
        return "HOLD"

    model = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)

    # ✅ Utilise les noms de features du modèle entraîné
    feature_names = model.feature_names_in_
    X_df = pd.DataFrame([X], columns=feature_names)

    prediction = model.predict(X_df)[0]
    return le.inverse_transform([prediction])[0]

def load_rf():
    if not os.path.exists(MODEL_PATH):
        return None, None
    return joblib.load(MODEL_PATH), joblib.load(ENCODER_PATH)