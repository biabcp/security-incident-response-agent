# Evaluation Plan

## Metrics
1. Retrieval relevance (top-k hit rate)
2. Hallucination rate (unsupported claims / reports)
3. Evidence citation accuracy
4. Response latency (ms per investigation)
5. False-positive risk proxy (high-risk output on benign cases)

## Method
- Replay queries from `data/test_cases/incident_queries.json`.
- Score outputs with deterministic validators in `src/evaluation/metrics.py`.
- Store periodic benchmark summaries for regression tracking.

## Acceptance targets
- Retrieval relevance >= 0.70
- Hallucination rate <= 0.05
- Citation accuracy >= 0.95
- Median latency <= 1500ms (local baseline)
