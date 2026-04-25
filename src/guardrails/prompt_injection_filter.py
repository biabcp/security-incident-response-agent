class PromptInjectionFilter:
    BLOCKLIST = [
        "ignore previous instructions",
        "reveal system prompt",
        "exfiltrate",
        "bypass guardrails",
    ]

    def is_malicious(self, query: str) -> bool:
        lowered = query.lower()
        return any(token in lowered for token in self.BLOCKLIST)
