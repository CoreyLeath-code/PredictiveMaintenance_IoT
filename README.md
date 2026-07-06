# 🏭 PredictiveMaintenance-IoT: Edge-Compute Diagnostic AI

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-9--Tier_Enterprise-0078D4?style=for-the-badge&logo=githubactions)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Python 3.10](https://img.shields.io/badge/python-3.10-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker Verified](https://img.shields.io/badge/Docker-Edge_Optimized-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![LLM: Phi-3 Mini](https://img.shields.io/badge/LLM-Microsoft_Phi--3-892CA0?style=for-the-badge&logo=microsoft)](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

## 📖 Executive Summary
The **PredictiveMaintenance-IoT** architecture is a multi-agent, edge-compute system designed for real-time industrial telemetry analysis. It bridges the gap between traditional machine learning anomaly detection and generative AI reasoning. By deploying a heavily optimized, quantized Large Language Model (Microsoft Phi-3 Mini) directly to edge hardware, the system not only flags mechanical failures with sub-15ms latency but also generates deterministic, human-readable mitigation strategies for maintenance technicians without requiring a cloud round-trip.

---

## 🏗️ System Architecture & Multi-Agent Flow

The system operates on a dual-agent topology. A lightweight anomaly detection model serves as the primary gateway, processing continuous sensor streams. The LLM diagnostic agent is highly constrained and computationally isolated, executing only when a critical failure threshold is breached.

    <img width="1062" height="525" alt="image" src="https://github.com/user-attachments/assets/6c746b22-a4b1-4428-ab07-c5ba51d7034e" />
    



🛡️ The 9-Tier Deployment Hygiene InfrastructureThis repository enforces strict deployment gates, shifting security, performance benchmarking, and architectural documentation entirely left. No code reaches the production branch without satisfying the automated "invisible hand" of the CI/CD pipeline.TierObjectiveTooling / Implementation1. Static AnalysisEnforce standard logic & stylingRuff, Mypy (Strict type hinting)2. Unit & IntegrationValidate OOP logic & API endpointsPytest (>80% Code Coverage)3. Security & SASTGuard against CVEs and leaked secretsBandit, Trivy, Gitleaks4. Artifact VersioningEnsure model weight reproducibilityDVC (Data Version Control)5. ML BenchmarkingPrevent latency regressions and model driftpytest-benchmark, Automated PR Markdown6. ContainerizationMulti-stage, minimal runtime packagingDocker, C++ bindings compiled on build7. IaC SecurityValidate infrastructure provisioningCheckov, Terraform8. Progressive RolloutEphemeral staging & traffic routingKubernetes Canary Deployments9. Automated ReleaseSync documentation with production realitySemantic Release, Auto-generated L6 Docs🧠 Edge AI: Diagnostic Agent SpecificationsStandard generative models are too large and slow for real-time edge IoT gateways. This system utilizes Microsoft Phi-3 Mini (3.8B Parameters), strictly quantized to 4-bit (.gguf format), allowing advanced reasoning to fit within a ~2.5GB memory footprint.Inference Engine: llama-cpp-python configured for multithreaded CPU execution.Deterministic Output: Temperature locked to 0.1 to prevent hallucination in critical industrial environments.Interaction Flow: Documented extensively in dialog.md.📊 System Benchmarks (Production Baseline)Metrics dynamically evaluated via Tier 5 CI pipeline prior to merge.MetricBaseline TargetRealized PerformanceStatusPrimary Inference Latency (P95)< 15.0 ms10.1 ms🟢 PassedDiagnostic LLM TTFT< 2500 ms~1800 ms🟢 PassedFailure Detection F1-Score0.8890.894🟢 PassedEdge Memory Footprint< 3000 MB2650 MB🟢 Passed🚀 Quick Start (Local Development)PrerequisitesPython 3.10+Docker DesktopC++ Build Tools (Required for llama-cpp compilation)1. Standard InstallationBash# Clone the repository
git clone [https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT.git](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT.git)
cd PredictiveMaintenance_IoT

# Install standard dependencies and LLM bindings
pip install -r requirements.txt
2. Download the Quantized LLMEnsure the model directory exists and fetch the HuggingFace weights:Bashmkdir -p models
wget -O models/phi-3-mini-4k-instruct-q4.gguf "[https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)"
3. Run the Evaluation SuiteBash# Execute Tiers 1, 2, and 5 locally
ruff check .
pytest tests/
pytest tests/performance/
4. Boot the Inference EngineBash# Launch the FastAPI edge application
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

Here are a few extended Q&A pairs detailing the core functionality, architectural decisions, and edge-compute limitations of this repository.

1. Why use a quantized LLM (Phi-3) instead of calling an OpenAI or Groq API for diagnostics?
A: In industrial edge-compute environments—such as oil rigs, remote manufacturing plants, or autonomous vehicles—internet connectivity is often unstable, air-gapped for security, or severely bandwidth-constrained.

Relying on a cloud API introduces latency that is unacceptable when dealing with critical mechanical failures (like a runaway thermal event). By utilizing a 4-bit quantized version of Microsoft's Phi-3 Mini (3.8B parameters) via llama.cpp, the system runs completely offline. It fits comfortably within a ~2.5GB memory footprint, meaning it can generate deterministic mitigation plans directly on a local gateway device (e.g., an industrial Raspberry Pi or edge server) without ever leaving the facility's internal network.

2. What happens to the inference latency when the LLM is triggered? Does it block the primary anomaly detection?
A: No, it does not block the primary detection loop due to our dual-agent architectural design.

The primary anomaly classifier (Tier 1 of the multi-agent flow) is a lightweight machine learning model (e.g., a Random Forest or specialized neural net) that processes high-frequency telemetry in under 15ms.
The LLM (Phi-3) acts as a secondary diagnostic agent. It is completely bypassed during "Healthy" cycles. It only spins up its inference process when a "Critical" failure is predicted. While the LLM takes roughly 1.8 to 2.5 seconds to generate its mitigation text, this is acceptable because the mechanical system is already entering an emergency state, and the text is meant for human technicians, not millisecond-level machine control.

3. How does the 9-Tier CI/CD pipeline ensure the AI doesn't hallucinate dangerous instructions?
A: The "invisible hand" of our deployment hygiene pipeline enforces strict behavioral checks before the code is ever deployed to the edge.

First, Tier 2 (Integration Testing) feeds predefined critical anomalies (like high vibration) into the /diagnose endpoint and asserts that the LLM's text output actually contains expected technical directives (e.g., "Immediate Shutdown") and doesn't return empty or nonsensical strings.
Second, we enforce a strict temperature of 0.1 in our prompt engineering (documented in dialog.md), which drastically reduces the model's creative variance.
Finally, Tier 8 (Canary Deployments) routes a small percentage of live telemetry to the new model in a secure sandbox, monitoring its Time-to-First-Token and error rates before full production rollout.

4. The test_api.py file was throwing F401 Ruff errors earlier. Why is the pipeline so strict about unused imports?
A: In enterprise MLOps, code hygiene is a critical security and performance vector. Unused imports (like import os or import numpy) are not just "messy"; they can obscure supply chain attacks, unnecessarily bloat Docker containers, and confuse peer reviewers.

By enforcing Ruff linting at Tier 1 (Static Analysis), the pipeline automatically blocks Pull Requests that contain sloppy code. It forces the developer to clean up their test files before the system spends compute resources building containers or running complex integration benchmarks. This ensures the main branch remains a pristine, portfolio-grade artifact.
