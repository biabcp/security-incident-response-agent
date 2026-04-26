import json

from src.evaluation.metrics import citation_accuracy, hallucination_rate, retrieval_relevance
from src.evaluation.test_runner import run_retrieval_eval


def test_metrics_are_computable():
    relevance = retrieval_relevance([{"message": "failed login"}], ["failed login"])
    hall = hallucination_rate(total_reports=20, unsupported_reports=1)
    cite = citation_accuracy(total_claims=10, cited_claims=9)

    assert relevance == 1.0
    assert hall == 0.05
    assert cite == 0.9


def test_run_retrieval_eval_handles_empty_cases(tmp_path):
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps([]), encoding="utf-8")

    summary = run_retrieval_eval(str(cases_path), "data/sample_logs")
    assert summary["mean_retrieval_relevance"] == 0.0
