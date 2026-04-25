from typing import List, Dict, Any


def retrieve_relevant(logs: List[Dict[str, Any]], query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    terms = query.lower().split()
    scored = []
    for log in logs:
        text = " ".join(str(v).lower() for v in log.values())
        score = sum(term in text for term in terms)
        if score > 0:
            scored.append((score, log))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]
