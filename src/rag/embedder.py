import math
import re
from typing import List


TOKEN_RE = re.compile(r"[a-z0-9]+")


def embed(text: str, dimensions: int = 128) -> List[float]:
    """Create a lightweight normalized embedding using hashed token features."""
    if not text:
        return [0.0] * dimensions

    vector = [0.0] * dimensions
    for token in TOKEN_RE.findall(text.lower()):
        index = hash(token) % dimensions
        vector[index] += 1.0

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        return vector
    return [value / norm for value in vector]
