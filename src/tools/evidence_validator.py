from typing import Any, Dict, List


class EvidenceValidator:
    def has_citations(self, report: str, evidence: List[Dict[str, Any]]) -> bool:
        if not evidence:
            return "Insufficient evidence." in report
        ids = [str(item.get("id", "")) for item in evidence if item.get("id")]
        return any(f"[{event_id}]" in report for event_id in ids)
