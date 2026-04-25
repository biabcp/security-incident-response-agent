# SDLC Documentation

## Requirements
Defined in README and tests:
- users: SOC analysts, incident responders, security engineers
- use cases: alert triage, suspicious auth investigation, host anomaly review
- outputs: risk score, cited evidence, recommendation, audit trail

## Secure design
- threat model maintained in `docs/threat-model.md`
- guardrails and evidence validation in code

## Implementation
- modular Python package structure
- secure defaults and typed state
- environment variable configuration only

## Verification
- unit + integration tests with adversarial coverage
- evaluation metrics for retrieval relevance and hallucination rate

## Deployment
- Docker and Compose included

## Monitoring
- structured audit logging + user feedback capture pattern

## Resume-ready project summary
Built a vendor-neutral Agentic AI Security Assistant in Python that triages security alerts using RAG retrieval, deterministic tool orchestration, risk scoring, guardrails, and human oversight. Designed with SDLC artifacts (architecture, threat model, testing strategy, evaluation framework) and implemented auditable JSONL action logging, adversarial prompt defenses, and evidence-grounded reporting for trustworthy SOC workflows.
