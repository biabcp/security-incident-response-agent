import json
from pathlib import Path
from typing import Any, Dict


class AuditLogger:
    def __init__(self, audit_path: str = "audit_logs/agent_audit.jsonl"):
        self.audit_path = Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, record: Dict[str, Any]) -> None:
        with self.audit_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, default=str) + "\n")
