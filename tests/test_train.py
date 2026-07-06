"""Unit tests for model training logic."""
import os
import pytest
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def sample_csv(tmp_path):
    """Write a minimal valid sensor CSV and return its path."""
    df = pd.DataFrame({
        "temperature": [70, 85, 78, 90, 72, 80, 65, 95],
        "vibration":   [0.02, 0.05, 0.03, 0.08, 0.01, 0.04, 0.01, 0.09],
        "pressure":    [1.5, 2.0, 1.7, 2.5, 1.3, 1.8, 1.2, 2.8],
        "failure":     [0, 1, 0, 1, 0, 0, 0, 1],
    })
    path = str(tmp_path / "sensor_data.csv")
    df.to_csv(path, index=False)
    return path


@pytest.fixture()
def mixed_case_csv(tmp_path):
    """CSV with mixed-case column headers to test normalisation."""
    df = pd.DataFrame({
        "Temperature": [70, 85],
        "Vibration":   [0.02, 0.05],
        "Pressure":    [1.5, 2.0],
        "Failure":     [0, 1],
    })
    path = str(tmp_path / "mixed_case.csv")
    df.to_csv(path, index=False)
    return path


# ---------------------------------------------------------------------------
# Tests for load_data
# ---------------------------------------------------------------------------

class TestLoadData:
    def test_loads_valid_csv(self, sample_csv):
        from models.train import load_data
        df = load_data(sample_csv)
        assert len(df) == 8
        assert set(["temperature", "vibration", "pressure", "failure"]).issubset(df.columns)

    def test_normalises_column_case(self, mixed_case_csv):
        from models.train import load_data
        df = load_data(mixed_case_csv)
        assert "temperature" in df.columns

    def test_raises_on_missing_file(self, tmp_path):
        from models.train import load_data
        with pytest.raises(FileNotFoundError):
            load_data(str(tmp_path / "nonexistent.csv"))

    def test_raises_on_missing_columns(self, tmp_path):
        from models.train import load_data
        df = pd.DataFrame({"temperature": [70], "vibration": [0.02]})
        path = str(tmp_path / "bad.csv")
        df.to_csv(path, index=False)
        with pytest.raises(ValueError, match="missing required columns"):
            load_data(path)


# ---------------------------------------------------------------------------
# Tests for train
# ---------------------------------------------------------------------------

class TestTrain:
    def test_returns_fitted_model(self, sample_csv):
        from models.train import load_data, train
        df = load_data(sample_csv)
        model = train(df)
        # Model should be able to predict on new data
        X_new = np.array([[75.0, 0.03, 1.6]])
        preds = model.predict(X_new)
        assert preds[0] in (0, 1)

    def test_model_has_predict_proba(self, sample_csv):
        from models.train import load_data, train
        df = load_data(sample_csv)
        model = train(df)
        X_new = np.array([[75.0, 0.03, 1.6]])
        proba = model.predict_proba(X_new)
        assert proba.shape == (1, 2)
        assert abs(proba[0].sum() - 1.0) < 1e-6


# ---------------------------------------------------------------------------
# Tests for save_model
# ---------------------------------------------------------------------------

class TestSaveModel:
    def test_saves_and_reloads(self, sample_csv, tmp_path):
        import joblib
        from models.train import load_data, train, save_model
        df = load_data(sample_csv)
        model = train(df)
        out_path = str(tmp_path / "out" / "model.pkl")
        save_model(model, out_path)
        assert os.path.exists(out_path)
        loaded = joblib.load(out_path)
        X_new = np.array([[70.0, 0.02, 1.5]])
        assert loaded.predict(X_new)[0] in (0, 1)
