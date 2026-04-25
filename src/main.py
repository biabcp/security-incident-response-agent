import argparse
from pathlib import Path

from src.agent.incident_agent import SecurityIncidentAgent
from src.audit.audit_logger import AuditLogger
from src.config import settings
from src.tools.log_search import LogSearchTool
from src.tools.risk_scoring import RiskScoringTool
from src.tools.threat_intel import ThreatIntelTool


def build_agent() -> SecurityIncidentAgent:
    data_path = Path(settings.data_dir)
    logs = LogSearchTool.load_jsonl_directory(data_path)
    return SecurityIncidentAgent(
        log_search_tool=LogSearchTool(logs),
        risk_scoring_tool=RiskScoringTool(),
        threat_intel_tool=ThreatIntelTool(),
        audit_logger=AuditLogger(settings.audit_log_path),
        review_threshold=settings.review_threshold,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic security incident response assistant")
    parser.add_argument("--query", required=True, help="Security alert or analyst question")
    parser.add_argument("--reviewer", default="system-auto", help="Reviewer ID for non-interactive review mode")
    args = parser.parse_args()

    agent = build_agent()
    state = agent.run(args.query, review_context={"mode": "auto", "reviewer": args.reviewer})
    print(state.final_report)


if __name__ == "__main__":
    main()
