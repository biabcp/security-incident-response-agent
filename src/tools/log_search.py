import json
import re
from pathlib import Path
from typing import Any, Dict, List

from src.rag.retriever import retrieve_relevant


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
        terms = [term for term in re.findall(r"[a-z0-9._-]+", query.lower()) if term]
        if not terms:
            return []
        matches: List[Dict[str, Any]] = []
        for log in self.logs:
            text = " ".join(str(v).lower() for v in log.values())
            if all(term in text for term in terms):
                matches.append(log)

        if matches:
            return matches[:max_results]
        # Fall back to semantic retrieval when strict lexical matching finds nothing.
        return retrieve_relevant(self.logs, query, top_k=max_results)
