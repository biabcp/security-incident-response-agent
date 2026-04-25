import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    audit_log_path: str = os.getenv("AUDIT_LOG_PATH", "audit_logs/agent_audit.jsonl")
    data_dir: str = os.getenv("DATA_DIR", "data/sample_logs")
    review_threshold: int = int(os.getenv("REVIEW_THRESHOLD", "70"))


settings = Settings()
