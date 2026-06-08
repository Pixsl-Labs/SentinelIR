import json
from pathlib import Path

from app.models.app_config import (
    AppConfig,
    ThresholdConfig,
    LiveMonitoringConfig,
    OutputConfig
)


def load_config(
            config_path: str = "sentinel_config.json"
    ) -> AppConfig:
    """
    Loads the SentinelIR application configuration.

    Reads the JSON configuration file, converts it into an AppConfig
    object, and applies default values for any missing optional sessions.

    Args:
        config_path (str): Path to the JSON configuration file.
            Defaults to "sentinel_config.json".

    Returns:
        AppConfig: Structured application configuration.
    """

    config_data = load_config_dict(
        config_path
    )

    return build_app_config(
        config_data
    )

def load_config_dict(
            config_path: str
    ) -> dict:
    """
    Reads raw configuration data from a JSON file.

    Args:
        config_path (str): Path to the JSON configuration file.

    Returns:
        dict: Raw configuration data loaded from the JSON file.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file contains invalid JSON.
    """

    path = Path(
        config_path
    )

    with path.open("r") as file:

        return json.load(file)

def build_app_config(
            config_data: dict
    ) -> AppConfig:
    """
    Builds an AppConfig object from raw dictionary data.

    Missing sections or values are replaced with sensible defaults from
    the AppConfig dataclasses.

    Args:
        config_data (dict): Raw configuration dictionary.

    Returns:
        AppConfig: Structured SentinelIR configuration object.
    """

    default_config = AppConfig()

    thresholds = config_data.get(
        "thresholds",
        {}
    )

    live_monitoring = config_data.get(
        "live_monitoring",
        {}
    )

    outputs = config_data.get(
        "outputs",
        {}
    )

    watched_files = config_data.get(
        "watched_files",
        default_config.watched_files
    )

    return AppConfig(
        watched_files=watched_files,

        thresholds=ThresholdConfig(
            brute_force_threshold=thresholds.get(
                "brute_force_threshold",
                default_config.thresholds.brute_force_threshold
            ),

            brute_force_time_window=thresholds.get(
                "brute_force_time_window",
                default_config.thresholds.brute_force_time_window
            ),

            user_targeting_threshold=thresholds.get(
                "user_targeting_threshold",
                default_config.thresholds.user_targeting_threshold
            )
        ),

        live_monitoring=LiveMonitoringConfig(
            poll_interval=live_monitoring.get(
                "poll_interval",
                default_config.live_monitoring.poll_interval
            ),

            status_interval=live_monitoring.get(
                "status_interval",
                default_config.live_monitoring.status_interval
            ),

            show_new_logs=live_monitoring.get(
                "show_new_logs",
                default_config.live_monitoring.show_new_logs
            )
        ),

        outputs=OutputConfig(
            reports_dir=outputs.get(
                "reports_dir",
                default_config.outputs.reports_dir
            ),

            logs_dir=outputs.get(
                "logs_dir",
                default_config.outputs.logs_dir
            )
        )
    )