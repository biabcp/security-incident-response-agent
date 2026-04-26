import re
from typing import Any, Dict, List


class EvidenceValidator:
    def has_citations(self, report: str, evidence: List[Dict[str, Any]]) -> bool:
        if not evidence:
            return "Insufficient evidence." in report
        valid_ids = {str(item.get("id", "")) for item in evidence if item.get("id")}
        if not valid_ids:
            return False

        cited_ids = {match.strip() for match in re.findall(r"\[([^\[\]]+)\]", report)}
        if not cited_ids:
            return False
        if not cited_ids.issubset(valid_ids):
            return False

        minimum_required = 1 if len(valid_ids) == 1 else 2
        coverage_ratio = len(cited_ids) / len(valid_ids)
        return len(cited_ids) >= minimum_required and coverage_ratio >= 0.5
