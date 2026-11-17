"""Streamlit Dashboard for PredictiveMaintenance-IoT."""

import os

import requests  # type: ignore
import streamlit as st

st.set_page_config(page_title="Edge AI Diagnostic Dashboard", layout="wide")

st.title("🏭 PredictiveMaintenance-IoT Command Center")
st.markdown("Monitor edge sensor streams and verify Multi-Agent diagnostic logic.")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")

st.sidebar.header("Simulator Controls")
sensor_id = st.sidebar.slider("Sensor ID", 100, 999, 101)
temp = st.sidebar.slider("Temperature (°C)", 20.0, 120.0, 45.0)
vib = st.sidebar.slider("Vibration (g)", 0.0, 10.0, 0.1)
anomaly = st.sidebar.toggle("Simulate Anomaly Detected", value=False)

if st.sidebar.button("Execute Diagnostic Request"):
    payload = {
        "sensor_id": sensor_id,
        "temperature": temp,
        "vibration": vib,
        "anomaly_detected": anomaly,
    }

    try:
        response = requests.post(f"{API_URL}/diagnose", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        st.subheader("Agent Output:")
        st.json(result)

        if "SAFETY OVERRIDE" in result.get("mitigation_plan", ""):
            st.error("Safety Monitor Intercepted Hazardous Instruction!")
        elif anomaly:
            st.success("Diagnostic plan generated.")
    except requests.RequestException:
        st.error("Diagnostic API is unavailable or returned an error.")

st.divider()
st.markdown("### Architecture Flow")
