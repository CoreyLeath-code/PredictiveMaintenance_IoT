# PredictiveMaintenance IoT

Documentation for the portfolio-scale C# ML.NET predictive-maintenance pipeline and separate Python FastAPI diagnostic gateway.

> **Evidence boundary:** the canary-deployment workflow is a portfolio simulation, not an AWS deployment. Passing its checks is not proof of production health, safety certification, or release readiness.

## Start here

- [Engineering decisions](engineering-decisions.md) — design trade-offs and boundaries
- [n8n automation](automation/N8N.md) — experimental workflow integration
- [Source repository and verified quick start](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT#quickstart--verified-cilocal-path)
- [Detailed engineering audit](https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT/blob/main/L6_AUDIT.md)

## Operational notes

The model inference path must fail closed when the reviewed model artifact is unavailable. The CI benchmark exercises the explicit mock diagnostic path and does not measure real Phi-3 token throughput. The Tier 9 job builds these docs and publishes to GitHub Pages; it deliberately **does not** create or sign a software release after a simulated canary run.
