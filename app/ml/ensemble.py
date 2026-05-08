from app.ml.random_forest import predict_rf
from app.ml.xgboost_model import predict_xgb


def ensemble_predict(X) -> dict:
    rf_signal = predict_rf(X)
    xgb_signal = predict_xgb(X)

    if rf_signal == xgb_signal:
        final_decision = rf_signal
        confidence = 1.0
    else:
        final_decision = "HOLD"
        confidence = 0.5

    return {
        "rf_signal": rf_signal,
        "xgb_signal": xgb_signal,
        "final_decision": final_decision,
        "confidence": confidence,
    }