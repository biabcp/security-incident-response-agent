import re


class PIIRedactor:
    EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    def redact(self, text: str) -> str:
        text = self.EMAIL_RE.sub("[REDACTED_EMAIL]", text)
        return self.IPV4_RE.sub("[REDACTED_IP]", text)
