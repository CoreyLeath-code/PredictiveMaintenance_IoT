"""Unit tests for the FastAPI prediction and diagnostic endpoints."""

import joblib
import numpy as np
from fastapi.testclient import TestClient

# Import the FastAPI app instance from your source code
# Note: Adjust the import path 'src.api.main' if your app is located in a different directory
from src.api.main import app 

client = TestClient(app)

def test_health_check():
    """Verify the API boots correctly. Essential for Tier 6 container validation."""
    response = client.get("/health")
    assert response.status_code == 200
    # Update the expected JSON below if your health endpoint returns something different
    assert response.json() == {"status": "healthy"}

def test_diagnostic_endpoint_healthy_sensor():
    """Verify the diagnostic agent bypasses the LLM when no anomaly is detected."""
    payload = {
        "sensor_id": 101,
        "temperature": 45.2,
        "vibration": 0.12,
        "anomaly_detected": False
    }
    
    response = client.post("/diagnose", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "Healthy"
    assert "None required" in data["mitigation"]

def test_diagnostic_endpoint_critical_anomaly():
    """Verify the diagnostic agent successfully generates a mitigation plan during a failure."""
    payload = {
        "sensor_id": 102,
        "temperature": 95.5,
        "vibration": 5.1,
        "anomaly_detected": True
    }
    
    response = client.post("/diagnose", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["sensor_id"] == 102
    assert "mitigation_plan" in data
    assert isinstance(data["mitigation_plan"], str)
    
    # Ensure the LLM actually generated text and didn't return an empty string
    assert len(data["mitigation_plan"]) > 0
