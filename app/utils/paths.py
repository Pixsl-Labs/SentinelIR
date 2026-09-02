from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = PROJECT_ROOT / "sentinel_config.json"

INPUT_LOGS_DIR = PROJECT_ROOT / "log_files"

APPLICATION_LOGS_DIR = PROJECT_ROOT / "logs"

APPLICATION_LOG_DIR = APPLICATION_LOGS_DIR / "sentinelir.log"

REPORTS_DIR = PROJECT_ROOT / "reports"
