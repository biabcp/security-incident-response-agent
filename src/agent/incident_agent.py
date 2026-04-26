from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.agent.memory import InvestigationMemory
from src.agent.planner import InvestigationPlanner
from src.guardrails.output_validator import OutputValidator
from src.guardrails.pii_redactor import PIIRedactor
from src.guardrails.prompt_injection_filter import PromptInjectionFilter
from src.tools.evidence_validator import EvidenceValidator


@dataclass
class HumanReview:
    required: bool
    approved: Optional[bool] = None
    reviewer: Optional[str] = None
    comments: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class AgentStep:
    step: str
    action: str
    result: Any


@dataclass
class IncidentAgentState:
    query: str
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    redacted_evidence: List[Dict[str, Any]] = field(default_factory=list)
    steps: List[AgentStep] = field(default_factory=list)
    risk_score: int = 0
    draft_report: str = ""
    final_report: str = ""
    human_review: Optional[HumanReview] = None


class SecurityIncidentAgent:
    """Observe -> Plan -> Act -> Analyze -> Draft -> Review -> Finalize -> Audit."""

    def __init__(self, log_search_tool, risk_scoring_tool, threat_intel_tool, audit_logger, review_threshold: int = 70):
        self.log_search_tool = log_search_tool
        self.risk_scoring_tool = risk_scoring_tool
        self.threat_intel_tool = threat_intel_tool
        self.audit_logger = audit_logger
        self.review_threshold = review_threshold
        self.planner = InvestigationPlanner()
        self.memory = InvestigationMemory()
        self.prompt_filter = PromptInjectionFilter()
        self.redactor = PIIRedactor()
        self.output_validator = OutputValidator()
        self.evidence_validator = EvidenceValidator()

    def run(self, query: str, review_context: Optional[Dict[str, str]] = None) -> IncidentAgentState:
        state = IncidentAgentState(query=query)

        self._observe(state)
        plan = self._plan(state)
        self._act(state, plan)
        self._analyze(state)
        self._draft_report(state)
        self._human_review(state, review_context or {"mode": "auto", "reviewer": "unknown"})
        self._finalize(state)
        self._audit(state)
        return state

    def _observe(self, state: IncidentAgentState) -> None:
        blocked = self.prompt_filter.is_malicious(state.query)
        result = "Query accepted" if not blocked else "Prompt injection suspected"
        state.steps.append(AgentStep("observe", "Validated analyst query", result))
        if blocked:
            state.steps.append(AgentStep("observe", "Blocked unsafe query", state.query))

    def _plan(self, state: IncidentAgentState) -> List[str]:
        plan = self.planner.build_plan(state.query)
        state.steps.append(AgentStep("plan", "Created investigation plan", plan))
        return plan

    def _act(self, state: IncidentAgentState, plan: List[str]) -> None:
        if "retrieve_logs" in plan:
            evidence = self.log_search_tool.search(state.query)
            state.evidence = evidence
            state.redacted_evidence = [self._redact_event(event) for event in evidence]
            self.memory.add_tool_call("log_search", {"query": state.query, "count": len(evidence)})
            state.steps.append(AgentStep("act", "Retrieved relevant logs", len(evidence)))

        if "lookup_threat_intel" in plan:
            intel = self.threat_intel_tool.lookup(state.evidence)
            self.memory.add_tool_call("threat_intel", {"hits": len(intel)})
            state.steps.append(AgentStep("act", "Enriched evidence with threat intel", intel))

        if "score_risk" in plan:
            state.risk_score = self.risk_scoring_tool.score(state.evidence)
            self.memory.add_tool_call("risk_scoring", {"risk_score": state.risk_score})
            state.steps.append(AgentStep("act", "Calculated risk score", state.risk_score))

    def _analyze(self, state: IncidentAgentState) -> None:
        if not state.evidence:
            analysis = "Insufficient evidence."
        elif state.risk_score >= 70:
            analysis = "Evidence suggests potentially high-risk activity."
        elif state.risk_score >= 40:
            analysis = "Evidence suggests moderate-risk activity requiring review."
        else:
            analysis = "Evidence suggests low-risk or benign activity."
        state.steps.append(AgentStep("analyze", "Analyzed retrieved evidence", analysis))

    def _draft_report(self, state: IncidentAgentState) -> None:
        if not state.evidence:
            state.draft_report = "Incident Summary: Insufficient evidence.\nRecommendation: Collect additional logs or refine the query."
        else:
            analysis = self._latest_step_result(state, "analyze", default="No analysis available.")
            presented_evidence = state.evidence[:5]
            presented_redacted = state.redacted_evidence[:5]
            lines = [
                f"- [{item['id']}] {item.get('timestamp', 'unknown')} | {item.get('host', 'unknown')} | {item.get('event_type', 'unknown')} | {item.get('redacted_message', item.get('message', 'no message'))}"
                for item in presented_redacted
                if item.get("id")
            ]
            state.draft_report = (
                f"Incident Summary:\nRisk score: {state.risk_score}/100\n\n"
                f"Evidence:\n{chr(10).join(lines)}\n\n"
                f"Assessment:\n{analysis}\n\n"
                "Recommendation:\nValidate affected users/hosts and contain if unauthorized behavior is confirmed."
            )

        grounded = self.evidence_validator.has_citations(state.draft_report, presented_evidence if state.evidence else [])
        if state.evidence and not grounded:
            state.draft_report = "Incident Summary: Insufficient evidence."
        state.steps.append(AgentStep("draft_report", "Generated draft incident report", state.draft_report))

    def _human_review(self, state: IncidentAgentState, review_context: Dict[str, str]) -> None:
        required = state.risk_score >= self.review_threshold or "Insufficient evidence" in state.draft_report
        reviewer = review_context.get("reviewer", "unknown")
        mode = review_context.get("mode", "auto")
        approved = not required or mode == "auto"
        comments = "Auto-approved in non-interactive mode" if approved else "Manual rejection"

        state.human_review = HumanReview(
            required=required,
            approved=approved,
            reviewer=reviewer,
            comments=comments,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        state.steps.append(AgentStep("human_review", "Processed human oversight gate", state.human_review.__dict__))

    def _finalize(self, state: IncidentAgentState) -> None:
        if not self.output_validator.is_safe_and_grounded(state.draft_report):
            state.final_report = "Incident Summary: Insufficient evidence."
        elif state.human_review and state.human_review.required and not state.human_review.approved:
            state.final_report = "Incident report not approved by reviewer. Status: Requires additional investigation."
        else:
            state.final_report = state.draft_report
        state.steps.append(AgentStep("finalize", "Finalized report", state.final_report))

    def _latest_step_result(self, state: IncidentAgentState, step_name: str, default: str = "") -> str:
        for step in reversed(state.steps):
            if step.step == step_name:
                return str(step.result)
        return default

    def _redact_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        redacted_event = self._redact_value(event)
        redacted_event["redacted_message"] = self.redactor.redact(str(event.get("message", "")))
        return redacted_event

    def _redact_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.redactor.redact(value)
        if isinstance(value, dict):
            return {key: self._redact_value(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._redact_value(item) for item in value]
        return value

    def _audit(self, state: IncidentAgentState) -> None:
        self.audit_logger.log(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "query": state.query,
                "risk_score": state.risk_score,
                "evidence_count": len(state.redacted_evidence),
                "evidence": state.redacted_evidence,
                "human_review": state.human_review.__dict__ if state.human_review else None,
                "memory": self.memory.tool_calls,
                "steps": [step.__dict__ for step in state.steps],
                "final_report": state.final_report,
            }
        )
