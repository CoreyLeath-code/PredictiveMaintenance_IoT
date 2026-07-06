"""Tier 5 Performance Benchmarking for the Phi-3 Diagnostic Agent."""

import time
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

@pytest.fixture
def critical_sensor_payload():
    """Provides a standard high-severity anomaly payload for testing."""
    return {
        "sensor_id": 104,
        "temperature": 92.5,
        "vibration": 4.82,
        "anomaly_detected": True
    }

def test_diagnose_endpoint_latency(benchmark, critical_sensor_payload):
    """Benchmarks the total round-trip response time of the Phi-3 endpoint.
    
    This ensures that diagnostic generations do not exceed our edge timeout threshold.
    """
    def run_inference():
        response = client.post("/diagnose", json=critical_sensor_payload)
        assert response.status_code == 200
        return response

    # Execute the benchmark loop across multiple iterations to calculate statistical stability
    result = benchmark(run_inference)
    
    # Assert performance threshold (e.g., must complete within 2500ms on local test runners)
    assert benchmark.stats.stats.mean < 2.5


def test_diagnostic_payload_throughput(critical_sensor_payload):
    """Measures processing speed parameters of the internal engine.
    
    Ensures that empty outputs or severe hangs are caught during the PR validation gate.
    """
    start_time = time.perf_counter()
    response = client.post("/diagnose", json=critical_sensor_payload)
    elapsed_time = time.perf_counter() - start_time
    
    data = response.json()
    assert "mitigation_plan" in data
    
    text_content = data["mitigation_plan"]
    assert len(text_content) > 0
    
    # Calculate rough generation speed metric for the pipeline log
    tokens_estimated = len(text_content.split())
    tokens_per_second = tokens_estimated / elapsed_time
    
    print(f"\n[BENCHMARK] Generated ~{tokens_estimated} tokens in {elapsed_time:.2f}s ({tokens_per_second:.1f} tok/sec)")
