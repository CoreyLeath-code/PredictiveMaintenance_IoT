"""Unit tests for the FastAPI prediction endpoint."""

import joblib
import numpy as np
from fastapi.testclient import TestClient

# Assuming your FastAPI app is initialized in src/api/main.py
# If your app path is different, update this import accordingly
from src.api.main import app 

client = TestClient(app)

def test_health_check():
    """Verify the API boots correctly."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_prediction_endpoint():
    """Verify the model returns a valid prediction for IoT sensor data."""
    # Mock IoT sensor payload (update feature names to match your schema)
    payload = {
        "features": [
            {"sensor_id": 1, "temperature": 45.2, "vibration": 0.12},
            {"sensor_id": 2, "temperature": 46.1, "vibration": 0.15}
        ]
    }
    
    response = client.post("/predict", json=payload)
    
    # Ensure the endpoint successfully processes the request
    assert response.status_code == 200
    
    # Ensure the response contains the expected prediction key
    data = response.json()
    assert "predictions" in data
    assert isinstance(data["predictions"], list)
