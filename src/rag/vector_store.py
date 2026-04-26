from dataclasses import dataclass
from typing import List


@dataclass
class VectorRecord:
    id: str
    text: str
    vector: List[float]


class InMemoryVectorStore:
    def __init__(self):
        self.records: List[VectorRecord] = []

    def upsert(self, record: VectorRecord) -> None:
        self.records.append(record)

    def all(self) -> List[VectorRecord]:
        return self.records

    def query(self, vector: List[float], top_k: int = 5) -> List[VectorRecord]:
        scored = []
        for record in self.records:
            score = sum(a * b for a, b in zip(record.vector, vector))
            if score > 0:
                scored.append((score, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:top_k]]
