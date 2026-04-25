from pathlib import Path

from src.tools.log_search import LogSearchTool


def test_log_search_returns_matches():
    logs = LogSearchTool.load_jsonl_directory(Path("data/sample_logs"))
    tool = LogSearchTool(logs)
    results = tool.search("failed login workstation-07")
    assert results
    assert any("workstation-07" in str(item) for item in results)
