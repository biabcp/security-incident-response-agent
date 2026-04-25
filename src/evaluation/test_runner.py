import json
import time
from pathlib import Path

from src.evaluation.metrics import latency_ms, retrieval_relevance, summarize
from src.tools.log_search import LogSearchTool


def run_retrieval_eval(cases_path: str, logs_path: str) -> dict:
    with Path(cases_path).open("r", encoding="utf-8") as handle:
        cases = json.load(handle)

    logs = LogSearchTool.load_jsonl_directory(Path(logs_path))
    tool = LogSearchTool(logs)

    scores = []
    start = time.perf_counter() * 1000
    for case in cases:
        found = tool.search(case["query"])
        scores.append(retrieval_relevance(found, case["expected_keywords"]))
    end = time.perf_counter() * 1000

    summary = {
        "mean_retrieval_relevance": sum(scores) / len(scores),
        "latency_ms": latency_ms(start, end),
    }
    return summarize(summary)
