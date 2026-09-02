from datetime import datetime
from pathlib import Path


from app.models.enums import AlertType


from app.utils.paths import ALERT_LOG_PATH


def write_alert_log(
        alert_type: AlertType,
        severity: str,
        service: str,
        entity: str,
        message: str,
        log_path: str | Path = ALERT_LOG_PATH
        ) -> None:
    """
    Writes a live alert to a persistent human-readable alert log file.

    Args:
        alert_type (str): Type of alert raised.
        severity (str): Alert severity.
        service (str): Source service linked to the alert.
        entity (str): Main entity linked to the alert, such as an IP or username.
        message (str): Alert details.
        log_path (str | Path): Destination alert log path.
            Defaults to ALERT_LOG_PATH.

    Returns:
        None
    """

    alert_log_path = Path(
        log_path
    )

    alert_log_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    clean_message = message.strip().replace(
        " | ",
        "\n            "
    )

    separator = "-" * 70

    line = (
        f"{separator}\n"
        f"Timestamp : {timestamp}\n"
        f"Severity  : {severity}\n"
        f"Alert Type: {alert_type}\n"
        f"Service   : {service}\n"
        f"Entity    : {entity}\n"
        f"Details   : {clean_message}\n"
        f"{separator}\n"
    )

    with alert_log_path.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(line)
