from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class InvestigationMemory:
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)

    def add_tool_call(self, tool: str, payload: Dict[str, Any]) -> None:
        self.tool_calls.append({"tool": tool, "payload": payload})
