from typing import List


class InvestigationPlanner:
    def build_plan(self, query: str) -> List[str]:
        base_plan = ["retrieve_logs", "lookup_threat_intel", "score_risk", "validate_evidence", "draft_report"]
        if "malware" in query.lower() or "privilege" in query.lower():
            return base_plan + ["require_human_review_if_high_risk"]
        return base_plan
