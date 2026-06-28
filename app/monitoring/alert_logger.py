from datetime import datetime
from pathlib import Path

def write_alert_log(
        alert_type: str,
        severity: str,
        service:str,
        entity: str,
        message: str,
        log_path: str = "logs/alerts.log"
    ) -> None:
    """
    Writes a live alert to a persistent alert log file.

    Returns:
        None
    """

    Path("logs").mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    line = (
        f"{timestamp} | "
        f"{severity} | "
        f"{alert_type} | "
        f"{service} | "
        f"{entity} | "
        f"{message.strip()} | "
    )

    with open(
        log_path,
        "a"
    ) as file:
        
        file.write(line)

