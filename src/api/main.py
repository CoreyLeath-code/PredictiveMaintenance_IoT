"""FastAPI Edge Gateway for Predictive Maintenance IoT."""

import os
from typing import Any, Dict, Optional, cast
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Predictive Maintenance & Diagnostic API")

# Define the expected path for the quantized Phi-3 model
MODEL_PATH = "./models/phi-3-mini-4k-instruct-q4.gguf"

# Explicitly type hint the LLM variable to allow None in CI environments
llm: Optional[Any] = None

# Graceful fallback for CI/CD testing environments
if os.path.exists(MODEL_PATH):
    from llama_cpp import Llama
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4
    )
else:
    print("Warning: Phi-3 model not found. Running in CI/Mock mode.")

class SensorData(BaseModel):
    """Schema for incoming IoT sensor telemetry."""
    sensor_id: int
    temperature: float
    vibration: float
    anomaly_detected: bool

@app.get("/health")
def health_check() -> Dict[str, str]:
    """Tier 6 container health validation endpoint."""
    return {"status": "healthy"}

@app.post("/diagnose")
def generate_mitigation_strategy(data: SensorData) -> Dict[str, Any]:
    """
    Multi-agent routing endpoint.
    Bypasses LLM if healthy, triggers Phi-3 inference if critical.
    """
    # Agent Routing: Bypass LLM if no anomaly is detected
    if not data.anomaly_detected:
        return {
            "status": "Healthy", 
            "mitigation": "None required."
        }

    # CI/CD Test Mode: Return deterministic mock if model is missing
    if llm is None:
        return {
            "sensor_id": data.sensor_id,
            "mitigation_plan": "1. [CI/TEST MODE] Initiate mock shutdown.\n2. [CI/TEST MODE] Perform mock inspection."
        }

    # Edge AI Mode: Generate localized mitigation strategy via Phi-3
    prompt = f"""<|system|>
You are an expert industrial maintenance AI. Analyze the sensor data and provide a concise, 3-step mitigation strategy for the technician. Do not hallucinate.
<|user|>
Sensor ID: {data.sensor_id}
Temperature: {data.temperature} C
Vibration: {data.vibration} g
Status: CRITICAL ANOMALY PREDICTED
<|assistant|>
"""

    # Execute deterministic text generation
    raw_output = llm(
        prompt, 
        max_tokens=150, 
        stop=["<|user|>", "\n\n"], 
        temperature=0.1
    )
    
    # Cast the output to a standard Dictionary to satisfy Mypy's strict indexable checks
    output = cast(Dict[str, Any], raw_output)

    return {
        "sensor_id": data.sensor_id,
        "mitigation_plan": output['choices'][0]['text'].strip()
    }
