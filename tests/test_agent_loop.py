from pathlib import Path

from src.agent.incident_agent import SecurityIncidentAgent
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
