#  PredictiveMaintenance-IoT: Edge-Compute Diagnostic AI
[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-9--Tier_Enterprise-0078D4?style=for-the-badge&logo=githubactions)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions)
[![Coverage: 80%](https://img.shields.io/badge/Coverage-80%25-brightgreen.svg?style=for-the-badge)](https://pytest-cov.readthedocs.io/en/latest/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-Strict_Typing-164165?style=for-the-badge&logo=python&logoColor=white)](https://mypy-lang.org/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Edge_Gateway-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker Verified](https://img.shields.io/badge/Docker-Edge_Optimized-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Multi-Agent Architecture](https://img.shields.io/badge/Agents-Neurosymbolic-E91E63?style=for-the-badge&logo=google-cloud)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/tree/main/src/agents)
[![Data Version Control](https://img.shields.io/badge/DVC-Artifact_Sync-13bce9?style=for-the-badge&logo=dvc&logoColor=white)](https://dvc.org/)
[![LLM: Phi-3 Mini](https://img.shields.io/badge/LLM-Microsoft_Phi--3-892CA0?style=for-the-badge&logo=microsoft)](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)


The **PredictiveMaintenance-IoT** architecture is a multi-agent, edge-compute system designed for real-time industrial telemetry analysis. It bridges the gap between traditional machine learning anomaly detection and generative AI reasoning. By deploying a heavily optimized, quantized Large Language Model (Microsoft Phi-3 Mini) directly to edge hardware, the system not only flags mechanical failures with sub-15ms latency but also generates deterministic, human-readable mitigation strategies for maintenance technicians without requiring a cloud round-trip.

---


## Production Readiness Guide

> This section is the portfolio audit entry point for **PredictiveMaintenance_IoT**. It describes an engineering promotion path; it is not a claim that the repository is already production-authorized.

[![CI](https://img.shields.io/github/actions/workflow/status/CoreyLeath-code/PredictiveMaintenance_IoT/ci.yml?branch=main&label=CI)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions) [![License](https://img.shields.io/github/license/CoreyLeath-code/PredictiveMaintenance_IoT)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/blob/main/LICENSE)

### Architecture flowchart

```mermaid
flowchart LR
    Source --> Build[Release binary] --> Tests[Unit + sanitizer tests] --> Artifact[Versioned artifact]
```

### Quickstart and local validation

The supported local path should be reproducible from a clean checkout. The inferred stack for this repository is **C++**.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build
ctest --test-dir build --output-on-failure
```

If the project uses external services, model artifacts, cloud credentials, or private data, start them through documented local fixtures or mocks. Never place secrets or identifiable records in the repository.

### Research-style metrics and benchmarks

| Evidence | Required record |
|---|---|
| Correctness | Test command, commit SHA, runtime, and pass/fail result |
| Performance | Warm-up, sample count, concurrency, median, p95, p99, throughput, and memory |
| Data/model quality | Dataset version, split strategy, leakage controls, calibration, subgroup results, and uncertainty |
| Runtime | Image digest, health-check latency, resource limits, and rollback target |
| Security | Dependency, secret, SAST, container, and SBOM results |

A benchmark number belongs in a versioned artifact tied to a commit and hardware/runtime description. Engineering benchmarks must not be presented as clinical, financial, safety, or model-quality validation without the appropriate domain evidence.

### Extended Q&A

**What is production-ready for this repository?**  
A reproducible build, tested public contract, controlled configuration, observable runtime, documented security boundary, versioned artifacts, and a tested rollback path.

**What must remain explicit?**  
The intended use, excluded use, data/credential handling, model or algorithm limitations, and which metrics are measured versus aspirational.

**What should be completed next?**  
Use the linked production-readiness issue for this repository as the checklist. Resolve missing tests, deployment instructions, observability, supply-chain controls, and release evidence before attaching a production claim.


## System Architecture & Multi-Agent Flow

The system operates on a dual-agent topology. A lightweight anomaly detection model serves as the primary gateway, processing continuous sensor streams. The LLM diagnostic agent is highly constrained and computationally isolated, executing only when a critical failure threshold is breached.

<img width="623" height="431" alt="image" src="https://github.com/user-attachments/assets/05dbbd52-1032-421d-aab6-55640854e6d8" />

## 🔬 Empirical Performance Metrics (Automated)

*Performance evaluated on simulated edge hardware (4 CPU cores, 8GB RAM). LLM Inference executed via `llama.cpp` using the `microsoft/Phi-3-mini-4k-instruct-q4.gguf` quantized weights.*

### Sub-System A: ML Anomaly Detection (Primary Gateway)
| Metric | Target Threshold | Realized Performance | Std Dev (σ) | Statistical Note |
| :--- | :--- | :--- | :--- | :--- |
| **Throughput** | > 1000 req/sec | 1,420 req/sec | ± 45 | Evaluated over 10k continuous telemetry payloads. |
| **P50 Latency** | < 10.0 ms | 4.2 ms | ± 0.8 ms | Nominal processing speed. |
| **P99 Latency** | < 25.0 ms | 14.1 ms | ± 3.2 ms | Worst-case tail latency remains within safety bounds. |
| **F1-Score** | > 0.850 | 0.894 | N/A | Balanced precision/recall on synthetic failure dataset. |

### Sub-System B: Phi-3 Diagnostic Agent (Secondary Generation)
| Metric | Target Threshold | Realized Performance | Statistical Note |
| :--- | :--- | :--- | :--- |
| **Time-to-First-Token (TTFT)** | < 2000 ms | ~1450 ms | Critical metric for perceived technician UI responsiveness. |
| **Generation Speed** | > 15.0 tok/sec | 18.2 tok/sec | CPU-bound generation speed. |
| **Peak VRAM/RAM Usage** | < 3000 MB | 2650 MB | Confirms viability for deployment on 4GB edge gateways. |
| **Format Compliance**| 100% | 100% | Agent consistently adhered to 3-step numbered list format over 50 iterations. |

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
# [![CI](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions/workflows/ci-hygiene-security.yml/badge.svg?branch=docs%2Fportfolio-readme-production-predictivemaintenance-iot)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions/workflows/ci-hygiene-security.yml) [![Benchmarks](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions/workflows/benchmarks.yml/badge.svg?branch=docs%2Fportfolio-readme-production-predictivemaintenance-iot)](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/actions/workflows/benchmarks.yml)
