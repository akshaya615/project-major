import os
import numpy as np
import pickle
import joblib
from fastapi import APIRouter, HTTPException

from api.schemas import AccidentInput, PredictionOutput
from api.services.weather_service import get_live_weather
from api.services.traffic_service import get_live_traffic

router = APIRouter(tags=["Prediction"])

# --------------------------------------------------
# PATH CONFIGURATION (FIXED)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "ml")

# --------------------------------------------------
# Load model once (FIXED PATHS)
# --------------------------------------------------
with open(os.path.join(MODEL_DIR, "xgb_model.pkl"), "rb") as f:
    xgb_model = pickle.load(f)

try:
    label_encoder = joblib.load(
        os.path.join(MODEL_DIR, "severity_label_encoder.pkl")
    )
except Exception:
    with open(os.path.join(MODEL_DIR, "severity_label_encoder.pkl"), "rb") as f:
        label_encoder = pickle.load(f)


# --------------------------------------------------
# Predict Severity
# --------------------------------------------------
@router.post("/predict-severity", response_model=PredictionOutput)
def predict_severity(data: AccidentInput):
    try:
        # 🔹 LIVE WEATHER
        weather = get_live_weather(data.latitude, data.longitude)

        rain = weather["rain"]
        visibility = weather["visibility"]
        weather_code = weather["weather_code"]

        # 🔹 LIVE TRAFFIC
        congestion = get_live_traffic(data.latitude, data.longitude)

        # 🔹 SIMPLE ROAD RISK SCORE
        road_risk = 1 if rain > 0 or congestion > 0.7 else 0

        # 🔹 FINAL FEATURE VECTOR (13 FEATURES)
        features = np.array([[ 
            data.speed_limit,
            data.hour,
            data.month,
            data.day_of_week,
            data.number_of_deaths,
            data.number_of_injuries,
            data.latitude,
            data.longitude,
            rain,
            visibility,
            weather_code,
            congestion,
            road_risk
        ]])

        probs = xgb_model.predict_proba(features)
        pred_class = int(np.argmax(probs))
        severity = int(label_encoder.inverse_transform([pred_class])[0])

        return {
            "severity_class": severity,
            "confidence": float(np.max(probs)),
            "model_used": "hybrid (live weather + traffic)"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))