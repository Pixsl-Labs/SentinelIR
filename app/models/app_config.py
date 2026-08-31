from dataclasses import dataclass, field

from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD,
    BRUTE_FORCE_TIME_WINDOW,
    USER_TARGETING_THRESHOLD
)


@dataclass
class ThresholdConfig:
    """
    Stores detection threshold configuration values.

    These values control when SentinelIR should treat authentication
    behaviour as suspicious, such as brute-force attempts or distributed
    user-targeting activity.
    """

    brute_force_threshold: int = BRUTE_FORCE_THRESHOLD
    brute_force_time_window: int = BRUTE_FORCE_TIME_WINDOW
    user_targeting_threshold: int = USER_TARGETING_THRESHOLD


@dataclass
class LiveMonitoringConfig:
    """
    Stores live monitoring configuration values.

    These settings control how often watched files are checked, how often
    status output is printed, and whether new log lines are displayed while
    monitoring is running.
    """

    poll_interval: float = 0.2
    status_interval: int = 10
    show_new_logs: bool = True


@dataclass
class OutputConfig:
    """
    Stores output directory configuration values.

    These values define where SentinelIR writes generated reports and
    application log files.
    """

    reports_dir: str = "reports"
    logs_dir: str = "logs"


@dataclass
class AppConfig:
    """
    Represents the full SentinelIR application configuration.

    This model combines watched log files, detection thresholds, live
    monitoring settings, and output paths into one structured object.
    """

    watched_files: list[str] = field(
        default_factory=lambda: ["log_files/generated.log"]
    )
    thresholds: ThresholdConfig = field(
        default_factory=ThresholdConfig
    )
    live_monitoring: LiveMonitoringConfig = field(
        default_factory=LiveMonitoringConfig
    )
    outputs: OutputConfig = field(
        default_factory=OutputConfig
    )
