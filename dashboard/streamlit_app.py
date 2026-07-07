"""Streamlit Dashboard for PredictiveMaintenance-IoT."""

import streamlit as st
import requests  # type: ignore

st.set_page_config(page_title="Edge AI Diagnostic Dashboard", layout="wide")

st.title("🏭 PredictiveMaintenance-IoT Command Center")
st.markdown("Monitor edge sensor streams and verify Multi-Agent diagnostic logic.")

# Sidebar Controls
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
        "anomaly_detected": anomaly
    }
    
    # Point this to your FastAPI container (localhost:8000 if running locally)
    try:
        response = requests.post("http://localhost:8000/diagnose", json=payload)
        result = response.json()
        
        st.subheader("Agent Output:")
        st.json(result)
        
        if "SAFETY OVERRIDE" in result.get("mitigation_plan", ""):
            st.error("Safety Monitor Intercepted Hazardous Instruction!")
        elif anomaly:
            st.success("Phi-3 Diagnostic Plan Generated.")
            
    except Exception as e:
        st.error(f"Failed to connect to Edge Gateway: {e}")

# Add a visual architecture summary
st.divider()
st.markdown("### Architecture Flow")
