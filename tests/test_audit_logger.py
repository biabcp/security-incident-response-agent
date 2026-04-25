import json
from pathlib import Path

from src.audit.audit_logger import AuditLogger


def test_audit_logger_writes_jsonl(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    logger = AuditLogger(str(path))
    logger.log({"event": "test", "ok": True})

    line = path.read_text(encoding="utf-8").strip()
    doc = json.loads(line)
    assert doc["event"] == "test"
    assert doc["ok"] is True
