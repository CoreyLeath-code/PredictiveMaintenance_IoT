"""Deterministic Safety Agent for verifying LLM diagnostic outputs."""

from typing import Dict, Any

class SafetyAgent:
    """
    Evaluates generative AI mitigation plans against physical safety constraints.
    Acts as a deterministic firewall to prevent hazardous instructions.
    """
    def __init__(self) -> None:
        # Define hardcoded physical safety boundaries
        self.critical_vibration_threshold = 5.0  # g-force

    def verify_and_override(self, sensor_data: Dict[str, Any], llm_mitigation_plan: str) -> str:
        """
        Validates the LLM's proposed plan. 
        Returns the original plan if safe, or an emergency override if unsafe.
        """
        vibration = float(sensor_data.get("vibration", 0.0))
        llm_text_lower = llm_mitigation_plan.lower()

        # Rule 1: Never restart a high-vibration system without manual mechanical inspection
        if vibration >= self.critical_vibration_threshold:
            # If the LLM hallucinates a safe action during a physical crisis:
            if "restart" in llm_text_lower or "reboot" in llm_text_lower or "continue" in llm_text_lower:
                return (
                    "⚠️ [SAFETY OVERRIDE INITIATED] ⚠️\n"
                    "1. IMMEDIATE EMERGENCY STOP.\n"
                    f"2. The primary agent suggested a restart, but vibration ({vibration}g) exceeds physical safety limits.\n"
                    "3. Do NOT restart the motor. Dispatch team for structural integrity validation."
                )

        # If no physical rules are violated, allow the LLM's plan to pass through
        return llm_mitigation_plan

# Instantiate a singleton of the agent to be imported by the API
safety_monitor = SafetyAgent()
