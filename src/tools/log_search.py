import json
from pathlib import Path
from typing import Any, Dict, List


class LogSearchTool:
    def __init__(self, logs: List[Dict[str, Any]]):
        self.logs = logs

    @staticmethod
    def load_jsonl_directory(path: Path) -> List[Dict[str, Any]]:
        logs: List[Dict[str, Any]] = []
        for file_path in sorted(path.glob("*.jsonl")):
            with file_path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        logs.append(json.loads(line))
        return logs

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        terms = [term for term in query.lower().split() if term]
        if not terms:
            return []
        matches: List[Dict[str, Any]] = []
        for log in self.logs:
            text = " ".join(str(v).lower() for v in log.values())
            if any(term in text for term in terms):
                matches.append(log)
        return matches[:max_results]
