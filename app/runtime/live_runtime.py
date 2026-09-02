from colorama import Fore


from app.monitoring.file_monitor import FileMonitor
from app.monitoring.live_event_processor import LiveEventProcessor


from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_stat_row
)
from app.utils.colours import (
    get_live_status_colour
)
from app.utils.paths import ALERT_LOG_PATH


from app.models.enums import (
    AlertType
)


class LiveRuntime:
    """
    Handles live monitoring runtime mode.

    This runtime starts live log monitoring, connects the file monitor to the live
    event processor, and prints a session summary when monitoring ends.
    """

    def __init__(
            self,
            analyser,
            reporter,
            log_file,
            show_new_logs: bool = True,
            status_interval: int = 10,
            poll_interval: float = 0.2,
            mode_title: str = "Live Monitoring Mode"
            ) -> None:
        """
        Initialises the live runtime.

        Args:
            analyser: Log analyser instance updated during live monitoring.
            reporter: Log reporter instance available for reporting workflows.
            log_file: Path to the log file being monitored.
            show_new_logs (bool): Whether new log lines should be printed while
                monitoring. Defaults to True.
            status_interval (int): Number of processed events between live status
                updates. Defaults to 10.
            poll_interval (float): Delay between checks for new file content.
                Defaults to 0.2.
            mode_title (str): Header title displayed when live monitoring starts.
                Defaults to "Live Monitoring Mode".

        Returns:
            None
        """

        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file
        self.show_new_logs = show_new_logs
        self.status_interval = status_interval
        self.poll_interval = poll_interval
        self.mode_title = mode_title

    def start(self) -> None:
        """
        Starts live monitoring mode.

        Creates a live event processor and file monitor, watches the configured log
        file, and prints a live monitoring summary when monitoring stops successfully.

        Returns:
            None
        """

        print_section_header(
            self.mode_title,
            Fore.GREEN
        )

        processor = LiveEventProcessor(
            analyser=self.analyser,
            show_new_logs=self.show_new_logs,
            status_interval=self.status_interval
        )

        monitor = FileMonitor(
            file_path=self.log_file,
            processor=processor,
            poll_interval=self.poll_interval
        )

        success = monitor.watch()

        if success:

            self.print_live_session_summary(processor)

        else:

            print_empty_message(
                "Monitoring failed."
            )

    def print_live_session_summary(
            self,
            processor
            ) -> None:
        """
        Prints a summary of the live monitoring session.

        Displays processed event statistics and alert count for brute-force,
        suspicious-success, and user-targeting detections.

        Args:
            processor: Live event processor containing processed event statistics.

        Returns:
            None
        """

        brute_force_alerts = self.analyser.detection_engine.get_alert_count(
            AlertType.BRUTE_FORCE
        )

        suspicious_success_alerts = self.analyser.detection_engine.get_alert_count(
            AlertType.SUSPICIOUS_SUCCESS
        )

        user_targeting_alerts = self.analyser.detection_engine.get_alert_count(
            AlertType.USER_TARGETING
        )

        print_section_header(
            "Live Monitoring Summary",
            Fore.GREEN
        )

        print(
            Fore.LIGHTYELLOW_EX
            + "Session Activity"
        )

        brute_force_colour = get_live_status_colour("brute_force", brute_force_alerts)

        suspicious_colour = get_live_status_colour("suspicious_success", suspicious_success_alerts)

        user_targeting_colour = get_live_status_colour("user_targeting", user_targeting_alerts)

        processor.print_session_activity()

        print(
            Fore.LIGHTYELLOW_EX
            + "Alert Summary"
        )

        print_stat_row(
            "Total alerts raised",
            self.analyser.detection_engine.get_total_alerts(),
            get_live_status_colour(
                "alerts_raised",
                self.analyser.detection_engine.get_total_alerts()
            ),
            28
        )

        print_stat_row(
            "Brute-force alerts",
            brute_force_alerts,
            brute_force_colour,
            28
        )

        print_stat_row(
            "Suspicious-success alerts",
            suspicious_success_alerts,
            suspicious_colour,
            28
        )

        print_stat_row(
            "User-targeting alerts",
            user_targeting_alerts,
            user_targeting_colour,
            28
        )

        print(
            Fore.LIGHTYELLOW_EX
            + "\nEvidence"
        )

        print_stat_row(
            "Alert log path",
            ALERT_LOG_PATH,
            Fore.CYAN,
            28
        )
