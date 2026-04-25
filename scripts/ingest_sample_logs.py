from pathlib import Path

from src.tools.log_search import LogSearchTool


def main() -> None:
    logs = LogSearchTool.load_jsonl_directory(Path("data/sample_logs"))
    print(f"Loaded {len(logs)} records.")


if __name__ == "__main__":
    main()
