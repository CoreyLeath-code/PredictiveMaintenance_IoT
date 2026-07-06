"""Unit tests for the multi-agent neurosymbolic safety logic."""

from src.agents.safety_agent import SafetyAgent

def test_safety_agent_allows_safe_plan():
    """Verify the agent permits standard LLM outputs under normal physical conditions."""
    agent = SafetyAgent()
    sensor_data = {"vibration": 1.2}
    llm_plan = "1. Isolate power. 2. Inspect bearings. 3. Restart system."
    
    verified_plan = agent.verify_and_override(sensor_data, llm_plan)
    assert verified_plan == llm_plan

def test_safety_agent_blocks_hazardous_plan():
    """Verify the agent intercepts and overrides hazardous LLM hallucinations."""
    agent = SafetyAgent()
    # Critical vibration threshold exceeded
    sensor_data = {"vibration": 6.1} 
    # LLM hallucinates a dangerous restart recommendation
    llm_plan = "1. Ignore the vibration. 2. Restart the motor immediately to maintain production."
    
    verified_plan = agent.verify_and_override(sensor_data, llm_plan)
    
    assert "SAFETY OVERRIDE" in verified_plan
    assert "IMMEDIATE EMERGENCY STOP" in verified_plan
    assert verified_plan != llm_plan
