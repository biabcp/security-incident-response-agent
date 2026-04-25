from src.evaluation.metrics import citation_accuracy, hallucination_rate, retrieval_relevance


def test_metrics_are_computable():
    relevance = retrieval_relevance([{"message": "failed login"}], ["failed login"])
    hall = hallucination_rate(total_reports=20, unsupported_reports=1)
    cite = citation_accuracy(total_claims=10, cited_claims=9)

    assert relevance == 1.0
    assert hall == 0.05
    assert cite == 0.9
