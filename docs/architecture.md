# Architecture

## System overview
The security incident response agent uses a modular, vendor-neutral architecture:
- **Interface Layer** (`src/main.py`): accepts analyst alert/question.
- **Agent Orchestrator** (`src/agent/incident_agent.py`): observe → plan → act → analyze → report → audit loop.
- **Tools Layer** (`src/tools/*`): log search, threat intel lookup, risk scoring, evidence validator.
- **RAG Layer** (`src/rag/*`): chunking, embedding abstraction, vector store, retrieval.
- **Guardrails** (`src/guardrails/*`): prompt injection filter, PII redactor, output validator.
- **Audit & Monitoring** (`src/audit/audit_logger.py`): JSONL action logging.
- **Evaluation Layer** (`src/evaluation/*`): quality and safety metrics.

## Data flow
1. Analyst query enters main entrypoint.
2. Guardrails pre-check query.
3. Planner builds deterministic investigation steps.
4. Retriever and log search collect candidate evidence.
5. Threat intel and risk scoring enrich the evidence.
6. Evidence validator checks references used in report.
7. Output validator blocks ungrounded claims.
8. Audit logger captures each action and final decision.

## Design principles
- Vendor-neutral interfaces and simple Python contracts.
- Least privilege and explicit tool invocation.
- Deterministic, testable logic for baseline reliability.
- Human oversight hooks for high-risk or low-evidence scenarios.
