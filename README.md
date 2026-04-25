# security-incident-response-agent

A GitHub-ready, vendor-neutral **Agentic AI Security Assistant** implemented in Python. It investigates security alerts using retrieval-augmented evidence, structured tool calls, guardrails, audit logging, and explicit evidence-based reasoning.

## Why this project
This project demonstrates SDLC-aligned security engineering for AI agents:
- requirements-driven design
- documented architecture and threat model
- secure coding controls
- testing and evaluation framework
- monitoring and auditability
- containerized deployment

## Core behavior
The agent follows:
1. Observe incoming alert/question.
2. Plan investigation steps.
3. Retrieve relevant logs (RAG-style retrieval over local corpus).
4. Call security tools (log search, threat intel, risk scoring, validation).
5. Analyze evidence.
6. Generate a structured incident summary.
7. Log every action for auditability.
8. Escalate to human oversight when needed.

If evidence is insufficient, the report explicitly returns: **"Insufficient evidence."**

## Repository structure
```text
security-incident-response-agent/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── docs/
├── data/
├── src/
├── tests/
└── scripts/
```

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/main.py --query "failed login privilege escalation on workstation-07"
```

## Run tests
```bash
pytest -q
```

## Run demo script
```bash
python scripts/run_demo.py
```

## Security controls implemented
- No hard-coded secrets; environment variable configuration via `src/config.py`.
- Input validation and prompt-injection pattern detection.
- PII redaction before evidence presentation.
- Output validator enforcing evidence-grounded language.
- Least-privilege design: tools are pure, bounded, and deterministic.
- Immutable JSONL audit trail for every investigation run.

## NVIDIA Agentic AI concept alignment
Mapped in `docs/nvidia-cert-mapping.md`:
- agent architecture
- planning
- tool use
- memory
- retrieval
- evaluation
- monitoring
- trustworthy AI
- human oversight

## Resume-ready summary
See `docs/sdlc.md` for a concise project summary suitable for resumes and interview storytelling.
