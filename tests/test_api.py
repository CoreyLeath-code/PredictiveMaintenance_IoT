"""Unit tests for the FastAPI prediction endpoint."""
import os
import sys
import types
import joblib
import numpy as np
import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Helpers – build a tiny trained model so tests don't need a real .pkl file
# ---------------------------------------------------------------------------

def _make_model(tmp_path):
    """Train a tiny RandomForestClassifier and save it; return the path."""
    from sklearn.ensemble import RandomForestClassifier

    X = np.array([[70, 0.02, 1.5], [85, 0.05, 2.0], [78, 0.03, 1.7],
                  [90, 0.08, 2.5], [72, 0.01, 1.3]])
    y = np.array([0, 1, 0, 1, 0])
    model = RandomForestClassifier(n_estimators=5, random_state=0)
    model.fit(X, y)
    path = str(tmp_path / "model.pkl")
    joblib.dump(model, path)
    return path


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Return a TestClient with a fresh model in a temp directory."""
    model_path = _make_model(tmp_path)
    monkeypatch.setenv("MODEL_PATH", model_path)

    # Reset cached model so the new path is used
    import api.main as main_module
    main_module._model = None
    monkeypatch.setattr(main_module, "MODEL_PATH", model_path)

    from api.main import app
    return TestClient(app)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestPredictEndpoint:
    def test_predict_normal_operation(self, client):
        payload = {"temperature": 70.0, "vibration": 0.02, "pressure": 1.5}
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "failure_risk" in data
        assert "probability" in data
        assert data["failure_risk"] in (0, 1)
        assert 0.0 <= data["probability"] <= 1.0

    def test_predict_high_risk_inputs(self, client):
        payload = {"temperature": 90.0, "vibration": 0.08, "pressure": 2.5}
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["failure_risk"] in (0, 1)

    def test_predict_missing_field_returns_422(self, client):
        payload = {"temperature": 75.0, "vibration": 0.03}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_temperature_too_high_returns_422(self, client):
        payload = {"temperature": 999.0, "vibration": 0.02, "pressure": 1.5}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_negative_vibration_returns_422(self, client):
        payload = {"temperature": 70.0, "vibration": -1.0, "pressure": 1.5}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_no_model_returns_503(self, tmp_path, monkeypatch):
        missing_path = str(tmp_path / "missing_model.pkl")
        monkeypatch.setenv("MODEL_PATH", missing_path)

        import api.main as main_module
        main_module._model = None
        monkeypatch.setattr(main_module, "MODEL_PATH", missing_path)

        from api.main import app
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        payload = {"temperature": 70.0, "vibration": 0.02, "pressure": 1.5}
        response = client_no_raise.post("/predict", json=payload)
        assert response.status_code == 503
