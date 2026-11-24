
# Security Policy

## Overview

PredictiveMaintenance_IoT is an AI-assisted predictive maintenance project combining C#/ML.NET components, a Python FastAPI diagnostic gateway, and optional local Phi-3 inference.

Security is an important part of the project's development lifecycle. This policy describes supported versions, vulnerability reporting, secure development practices, and responsible disclosure.

**Important:** This project is a portfolio-scale engineering implementation. It is not certified for safety-critical industrial operations or autonomous machinery control.

## Supported Versions

Security fixes are prioritized for the latest maintained release and the `main` development branch.

| Version | Supported |
| --- | --- |
| Latest maintained release | ✅ |
| `main` branch | ✅ |
| Older releases | Best effort |
| Deprecated or archived versions | ❌ |

Support means that security reports will be reviewed and fixes considered. It does not guarantee a specific response or remediation deadline.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately.

### Preferred Reporting Method

1. Navigate to the repository's **Security** tab.
2. Select **Advisories**, if available.
3. Choose **Report a vulnerability**.
4. Submit a private security report.

Repository:

https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT

If private vulnerability reporting is unavailable, contact the repository maintainer through an appropriate private channel listed on their GitHub profile.

Maintainer:

https://github.com/CoreyLeath-code

**Do not disclose unpatched vulnerabilities in public GitHub issues, discussions, or pull requests.**

### Include in Your Report

Where possible, provide:

- A clear description of the vulnerability.
- Affected files, components, and versions.
- Reproduction steps.
- Potential security impact.
- Relevant logs or screenshots with secrets removed.
- A proof of concept, if safe to share.
- Suggested remediation, if known.

Do not submit passwords, API keys, access tokens, private model artifacts, or sensitive industrial telemetry.

## Vulnerability Response Process

Reported vulnerabilities will be handled through the following process:

1. **Triage:** Review the report and determine whether the issue is reproducible.
2. **Assessment:** Evaluate severity, affected components, exploitability, and potential impact.
3. **Remediation:** Develop a targeted fix on an appropriate branch.
4. **Validation:** Run applicable tests, security scans, and regression checks.
5. **Release:** Publish or merge a validated security correction.
6. **Disclosure:** Coordinate disclosure once remediation and relevant user guidance are available.

Response times depend on maintainer availability and the complexity of the reported issue.

## Security Controls

### 1. Dependency Security

Python and .NET dependencies should be reviewed for known security vulnerabilities.

Security practices include:

- Reviewing Dependabot alerts and dependency update pull requests.
- Applying available security patches.
- Reviewing transitive dependencies.
- Avoiding vulnerable or unmaintained packages where practical.
- Validating dependency compatibility before merging updates.

Example Python dependency verification:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

### 2. Container Security

The project uses Docker for application packaging and execution.

The container security approach includes:

- Running the application as a non-root user.
- Maintaining patched operating system packages.
- Reducing unnecessary runtime dependencies.
- Keeping model weights outside the published container image.
- Scanning images for known vulnerabilities.
- Reviewing container build and publication workflows.

Container scanning is configured through:

- `.github/workflows/container-scan.yml`
- `.github/workflows/trivy.yml`

The Trivy workflows are designed to fail when fixable HIGH or CRITICAL vulnerabilities are detected.

Security findings should be remediated rather than hidden by disabling checks.

### 3. Continuous Integration Security

GitHub Actions supports automated development and security validation.

Depending on the workflow, checks may include:

- Python unit tests.
- Static analysis.
- Code hygiene checks.
- Dependency vulnerability scanning.
- Container vulnerability scanning.
- Security-related workflow validation.
- Software Bill of Materials (SBOM) generation.

A workflow being configured does not guarantee that its checks are passing. Security status should be verified against the latest completed GitHub Actions run.

### 4. API Security

The FastAPI diagnostic gateway exposes application endpoints including:

- `GET /health`
- `GET /ready`
- `POST /diagnose`

The gateway is intended for controlled development and evaluation environments.

Before exposing the API to untrusted networks, additional controls are required, including:

- Authentication and authorization.
- TLS termination.
- Rate limiting.
- Request-size restrictions.
- Input validation.
- Audit logging and sensitive-data redaction.
- Appropriate network access controls.

Do not treat the current API as an authenticated, production-ready public service.

### 5. AI Model Security

The optional Phi-3 inference backend introduces additional security considerations.

Recommended controls include:

- Reviewing model sources and licenses.
- Verifying model artifacts with SHA-256 checksums.
- Avoiding mutable model download references.
- Restricting access to model files.
- Treating model-generated responses as untrusted.
- Evaluating prompt injection and malicious input scenarios.
- Applying deterministic validation to safety-sensitive outputs.

Model-generated diagnostic recommendations must not directly operate industrial equipment without independent validated safety controls.

### 6. Diagnostic Safety

Predictive maintenance outputs are advisory.

The software must not be represented as a certified industrial safety system.

Current safeguards include explicit handling of unavailable diagnostic backends and separate health/readiness behavior.

The `ALLOW_MOCK_DIAGNOSTICS` configuration is intended for controlled testing and local development.

Mock results must not be presented as verified production diagnostic evidence.

### 7. Secrets Management

Do not commit sensitive information to source control.

Examples include:

- API keys.
- Authentication tokens.
- Cloud credentials.
- Database passwords.
- Private certificates.
- Deployment secrets.
- Sensitive equipment or industrial telemetry.

Use GitHub Actions secrets or another appropriate secret-management service when credentials are required.

If a secret is exposed:

1. Revoke or rotate the credential.
2. Determine the affected systems.
3. Remove the secret from active configuration.
4. Assess whether repository history requires remediation.
5. Document and review the incident privately.

Removing a secret from the latest commit does not automatically invalidate the exposed credential.

## Security Testing

Contributors can run applicable development checks before submitting changes.

### Python Tests

```bash
python -m pytest -q tests/
```

Where the tests explicitly require the mock diagnostic backend:

```bash
ALLOW_MOCK_DIAGNOSTICS=true python -m pytest -q tests/
```

### Container Build

```bash
docker build -t predictive-maintenance-iot:security-test .
```

### Container Vulnerability Scan

With Trivy installed:

```bash
trivy image \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  --exit-code 1 \
  predictive-maintenance-iot:security-test
```

A nonzero Trivy exit code requires investigation. Do not assume that every scanner failure is a confirmed vulnerability without reviewing the detailed logs.

## Pull Request Security Requirements

Security-sensitive pull requests should:

1. Describe the problem and affected components.
2. Include an appropriate regression test when feasible.
3. Preserve existing security controls.
4. Avoid introducing hardcoded credentials.
5. Verify affected dependencies and container images.
6. Complete applicable CI checks.
7. Document significant changes to security behavior.

Security checks must not be bypassed solely to achieve a passing workflow.

## Responsible Disclosure

Security researchers and contributors are encouraged to follow coordinated disclosure practices.

Please:

- Avoid disrupting live services.
- Do not access or modify data without authorization.
- Avoid destructive testing.
- Report vulnerabilities privately.
- Allow reasonable time for investigation and remediation before public disclosure.

## Security Limitations

The repository does not claim:

- Industrial safety certification.
- Verified resistance to every cyberattack.
- Production-grade authentication or multi-tenant isolation.
- Complete validation of AI-generated mitigation recommendations.
- Guaranteed incident response times.
- Zero known or future vulnerabilities.

Security maturity is an ongoing engineering objective, not a completed certification.

## Maintainer

**Corey Leath**

GitHub: https://github.com/CoreyLeath-code

Repository: https://github.com/CoreyLeath-code/PredictiveMaintenance_IoT

Security contributions and responsible vulnerability reports are welcome.

---

**Last reviewed:** November 2026
