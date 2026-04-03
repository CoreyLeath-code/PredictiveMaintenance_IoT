import logging
import os

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Predictive Maintenance IoT API", version="1.0.0")

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")

_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                f"Model file not found at '{MODEL_PATH}'. "
                "Run models/train.py to generate it first."
            )
        logger.info("Loading model from %s", MODEL_PATH)
        _model = joblib.load(MODEL_PATH)
    return _model


class SensorInput(BaseModel):
    temperature: float = Field(..., ge=-50.0, le=300.0, description="Temperature in °C")
    vibration: float = Field(..., ge=0.0, le=100.0, description="Vibration in mm/s")
    pressure: float = Field(..., ge=0.0, le=1000.0, description="Pressure in psi")


class PredictionOutput(BaseModel):
    failure_risk: int
    probability: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: SensorInput):
    try:
        model = get_model()
    except RuntimeError as exc:
        logger.error("Model unavailable: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc))

    features = np.array([[data.temperature, data.vibration, data.pressure]])
    try:
        prediction = model.predict(features)
        probability = float(model.predict_proba(features)[0][1])
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction error: {exc}")

    result = int(prediction[0])
    logger.info(
        "Prediction: temp=%.2f vib=%.4f pres=%.2f -> risk=%d prob=%.4f",
        data.temperature, data.vibration, data.pressure, result, probability,
    )
    return PredictionOutput(failure_risk=result, probability=probability)
