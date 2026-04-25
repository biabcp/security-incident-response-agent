from typing import List


def chunk_text(text: str, size: int = 200) -> List[str]:
    return [text[i : i + size] for i in range(0, len(text), size)] if text else []
