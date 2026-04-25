from typing import Any, Dict, List


class RiskScoringTool:
    def score(self, evidence: List[Dict[str, Any]]) -> int:
        if not evidence:
            return 0
        score = 0
        for event in evidence:
            severity = str(event.get("severity", "")).lower()
            message = str(event.get("message", "")).lower()
            event_type = str(event.get("event_type", "")).lower()
            if severity == "critical":
                score += 40
            elif severity == "high":
                score += 25
            elif severity == "medium":
                score += 10
            if "failed login" in message:
                score += 10
            if "privilege" in message or "privilege" in event_type:
                score += 20
            if "malware" in message:
                score += 30
            if "suspicious" in message:
                score += 15
            if "known malicious" in message:
                score += 20
        return min(score, 100)
