import logging
import os
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

REQUIRED_COLUMNS = {"temperature", "vibration", "pressure", "failure"}
DATA_PATH = os.getenv("DATA_PATH", "sensor_data.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")


def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training data not found at '{path}'")
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Training CSV is missing required columns: {missing}")
    return df


def train(df: pd.DataFrame) -> RandomForestClassifier:
    X = df[["temperature", "vibration", "pressure"]]
    y = df["failure"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logger.info("Test accuracy: %.4f", acc)
    logger.info("Classification report:\n%s", classification_report(y_test, y_pred, zero_division=0))

    return model


def save_model(model: RandomForestClassifier, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    joblib.dump(model, path)
    logger.info("Model saved to %s", path)


if __name__ == "__main__":
    try:
        logger.info("Loading data from %s", DATA_PATH)
        df = load_data(DATA_PATH)
        logger.info("Loaded %d rows", len(df))

        model = train(df)
        save_model(model, MODEL_PATH)
    except (FileNotFoundError, ValueError) as exc:
        logger.error("Training failed: %s", exc)
        sys.exit(1)
