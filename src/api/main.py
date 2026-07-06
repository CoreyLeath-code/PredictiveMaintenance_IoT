from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI(title="Predictive Maintenance & Diagnostic API")

# Initialize the quantized Phi-3 model (loaded into memory on startup)
# Ensure you download 'phi-3-mini-4k-instruct-q4.gguf' to the /models directory
llm = Llama(
    model_path="./models/phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=2048,  # Context window
    n_threads=4  # Optimize for edge CPU
)

class SensorData(BaseModel):
    sensor_id: int
    temperature: float
    vibration: float
    anomaly_detected: bool

@app.post("/diagnose")
def generate_mitigation_strategy(data: SensorData):
    if not data.anomaly_detected:
        return {"status": "Healthy", "mitigation": "None required."}

    # Construct the strict prompt for the LLM
    prompt = f"""<|system|>
You are an expert industrial maintenance AI. Analyze the sensor data and provide a concise, 3-step mitigation strategy for the technician. Do not hallucinate.
<|user|>
Sensor ID: {data.sensor_id}
Temperature: {data.temperature} C
Vibration: {data.vibration} g
Status: CRITICAL ANOMALY PREDICTED
<|assistant|>
"""

    # Generate the response using Phi-3
    output = llm(
        prompt,
        max_tokens=150,
        stop=["<|user|>", "\n\n"],
        temperature=0.1 # Keep it highly deterministic, no creative guessing
    )

    return {
        "sensor_id": data.sensor_id,
        "mitigation_plan": output['choices'][0]['text'].strip()
    }
