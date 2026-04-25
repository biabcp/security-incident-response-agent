from typing import Any, Dict, List


class ThreatIntelTool:
    MALICIOUS_INDICATORS = {
        "198.51.100.10": "Known C2 endpoint",
        "trojan": "Known malware family indicator",
        "encoded powershell": "Likely living-off-the-land execution pattern",
    }

    def lookup(self, evidence: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        findings: List[Dict[str, str]] = []
        for event in evidence:
            haystack = " ".join(str(v).lower() for v in event.values())
            for indicator, reason in self.MALICIOUS_INDICATORS.items():
                if indicator in haystack:
                    findings.append({"event_id": event.get("id", "unknown"), "indicator": indicator, "reason": reason})
        return findings
