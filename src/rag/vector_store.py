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
