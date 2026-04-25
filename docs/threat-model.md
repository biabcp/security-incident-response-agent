# Threat Model

## Scope
Threat model focuses on agent misuse, data protection, and decision integrity.

## Primary threats
1. **Prompt injection**
   - Risk: attacker manipulates query/instructions to bypass controls.
   - Mitigations: prompt injection filter, fixed tool plan, output validation.

2. **Data leakage**
   - Risk: sensitive fields exposed in report/audit output.
   - Mitigations: PII redaction, scoped logging, environment-based config.

3. **Hallucination / fabricated evidence**
   - Risk: report includes unsupported claims.
   - Mitigations: evidence validator + output validator requiring evidence IDs; fallback to “Insufficient evidence.”

4. **Unsafe tool use**
   - Risk: tool misuse causing unauthorized access/modification.
   - Mitigations: read-only local tools, bounded result sets, no shell command tools.

5. **Over-permissioned access**
   - Risk: broad filesystem/network access in production deployments.
   - Mitigations: containerization, least-privilege runtime identity, explicit data directory mounting.

## Residual risks
- Log poisoning in source systems.
- Analyst over-reliance without corroboration.
- Need for enterprise IAM integration in production.

## Security requirements
- Always preserve evidence provenance.
- Never invent unknown events.
- Escalate uncertain outcomes to human review.
