from typing import Dict, List


def retrieval_relevance(retrieved: List[dict], expected_keywords: List[str]) -> float:
    if not expected_keywords:
        return 1.0 if not retrieved else 0.5
    if not retrieved:
        return 0.0
    matched = 0
    corpus = " ".join(" ".join(str(v).lower() for v in item.values()) for item in retrieved)
    for key in expected_keywords:
        if key.lower() in corpus:
            matched += 1
    return matched / len(expected_keywords)


def hallucination_rate(total_reports: int, unsupported_reports: int) -> float:
    if total_reports <= 0:
        return 0.0
    return unsupported_reports / total_reports


def citation_accuracy(total_claims: int, cited_claims: int) -> float:
    if total_claims <= 0:
        return 1.0
    return cited_claims / total_claims


def false_positive_risk(high_risk_on_benign: int, benign_cases: int) -> float:
    if benign_cases <= 0:
        return 0.0
    return high_risk_on_benign / benign_cases


def latency_ms(start_ms: float, end_ms: float) -> float:
    return max(0.0, end_ms - start_ms)


def summarize(metrics: Dict[str, float]) -> Dict[str, float]:
    return {k: round(v, 4) for k, v in metrics.items()}
