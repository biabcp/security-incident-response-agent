import json
import math
import re
from typing import Any, Dict, List

from src.rag.embedder import embed
from src.rag.vector_store import InMemoryVectorStore, VectorRecord


def retrieve_relevant(logs: List[Dict[str, Any]], query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    terms = [term for term in re.findall(r"[a-z0-9._-]+", query.lower()) if term]
    if not terms:
        return []

    store = InMemoryVectorStore()
    id_to_log: Dict[str, Dict[str, Any]] = {}
    for idx, log in enumerate(logs):
        log_id = str(log.get("id", idx))
        text = json.dumps(log, sort_keys=True, default=str)
        id_to_log[log_id] = log
        store.upsert(VectorRecord(id=log_id, text=text, vector=embed(text)))

    query_vector = embed(query)
    min_term_matches = max(1, math.ceil(len(terms) * 0.6))
    vector_hits = store.query(query_vector, top_k=max(top_k * 3, top_k))
    ranked: List[tuple[int, Dict[str, Any]]] = []
    for record in vector_hits:
        log = id_to_log.get(record.id)
        if not log:
            continue
        text = " ".join(str(value).lower() for value in log.values())
        lexical_score = sum(term in text for term in terms)
        if lexical_score >= min_term_matches:
            ranked.append((lexical_score, log))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:top_k]]
