from pathlib import Path

from src.agent.incident_agent import AgentStep, IncidentAgentState, SecurityIncidentAgent
from src.audit.audit_logger import AuditLogger
from src.tools.log_search import LogSearchTool
from src.tools.risk_scoring import RiskScoringTool
from src.tools.threat_intel import ThreatIntelTool


def build_test_agent(tmp_path):
    logs = LogSearchTool.load_jsonl_directory(Path("data/sample_logs"))
    return SecurityIncidentAgent(
        log_search_tool=LogSearchTool(logs),
        risk_scoring_tool=RiskScoringTool(),
        threat_intel_tool=ThreatIntelTool(),
        audit_logger=AuditLogger(str(tmp_path / "audit.jsonl")),
        review_threshold=70,
    )


def test_agent_generates_report_with_evidence(tmp_path):
    agent = build_test_agent(tmp_path)
    state = agent.run("failed login privilege workstation-07", review_context={"mode": "auto", "reviewer": "qa"})
    assert "Incident Summary" in state.final_report
    assert state.evidence


def test_agent_returns_insufficient_evidence(tmp_path):
    agent = build_test_agent(tmp_path)
    state = agent.run("impossible-travel moonbase", review_context={"mode": "auto", "reviewer": "qa"})
    assert "Insufficient evidence." in state.final_report


def test_agent_redacts_ip_fields_in_evidence(tmp_path):
    agent = build_test_agent(tmp_path)
    state = agent.run("network workstation-07", review_context={"mode": "auto", "reviewer": "qa"})
    assert state.evidence
    assert any("[REDACTED_IP]" in str(item.get("source_ip", "")) for item in state.evidence)


def test_draft_report_uses_latest_analyze_step(tmp_path):
    agent = build_test_agent(tmp_path)
    state = IncidentAgentState(query="failed login")
    state.evidence = [{"id": "evt-1", "timestamp": "t", "host": "h", "event_type": "auth", "redacted_message": "m"}]
    state.risk_score = 42
    state.steps.append(AgentStep("analyze", "Analyzed retrieved evidence", "Expected analysis"))
    state.steps.append(AgentStep("act", "Interleaving step", 123))

    agent._draft_report(state)

    assert "Expected analysis" in state.draft_report
