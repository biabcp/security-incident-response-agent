from typing import List


def embed(text: str) -> List[float]:
    if not text:
        return [0.0]
    return [float(sum(ord(c) for c in text) % 997) / 997.0]
