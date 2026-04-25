# Testing Strategy

## Test layers
- **Unit tests**: agent loop, guardrails, log search, risk scoring, audit logger.
- **Integration tests**: end-to-end query to final report flow.
- **Adversarial tests**: prompt injection patterns and hallucination prevention.
- **Retrieval quality tests**: ensure relevant log events are returned.
- **Audit logging tests**: validate complete action trail persistence.

## Key assertions
- Agent returns “Insufficient evidence.” when no evidence is found.
- Reports only contain claims tied to evidence entries.
- High-risk cases trigger human oversight metadata.
- Audit entries capture step-by-step action history.
