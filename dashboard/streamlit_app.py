import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000") + "/predict"
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

st.set_page_config(page_title="Predictive Maintenance Dashboard", layout="wide")

st.title("🏭 Predictive Maintenance IoT Dashboard")

st.markdown("Enter sensor readings to predict equipment failure risk.")

# Sensor inputs
temperature = st.slider("Temperature (°C)", 0.0, 150.0, 75.0)
vibration = st.slider("Vibration (mm/s)", 0.0, 50.0, 10.0)
pressure = st.slider("Pressure (psi)", 0.0, 300.0, 120.0)

if st.button("Predict Failure Risk"):
    payload = {
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        result = response.json()

        failure_risk = result["failure_risk"]
        probability = result.get("probability", None)

        if failure_risk == 1:
            msg = "⚠ High Risk of Equipment Failure"
            if probability is not None:
                msg += f" (probability: {probability:.1%})"
            st.error(msg)
        else:
            msg = "✅ Equipment Operating Normally"
            if probability is not None:
                msg += f" (probability: {probability:.1%})"
            st.success(msg)

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the prediction API. Is it running?")
    except requests.exceptions.Timeout:
        st.error("⏱ Request timed out. The API may be overloaded.")
    except requests.exceptions.HTTPError as exc:
        st.error(f"API returned an error: {exc.response.status_code} {exc.response.text}")
    except (KeyError, ValueError) as exc:
        st.error(f"Unexpected response format from API (missing or invalid fields): {exc}")
