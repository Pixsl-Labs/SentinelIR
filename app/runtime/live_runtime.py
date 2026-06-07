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

from app.detection.alert_types import (
    BRUTE_FORCE_ALERT,
    SUSPICIOUS_SUCCESS_ALERT,
    USER_TARGETING_ALERT
)

from colorama import Fore


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
            log_file
        ):
        """
        Initialises the live runtime.

        Args:
            analyser: Log analyser instance updated during live monitoring.
            reporter: Log reporter instance available for reporting workflows.
            log_file: Path to the log file being monitored.

        Returns:
            None
        """

        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(self):
        """
        Starts live monitoring mode.

        Creates a live event processor and file monitor, watches the configured log
        file, and prints a live monitoring summary when monitoring stops successfully.

        Returns:
            None
        """

        print_section_header(
            "Live Monitoring Mode",
            Fore.GREEN
        )

        processor = LiveEventProcessor(
            analyser=self.analyser
        )

        monitor = FileMonitor(
            file_path=self.log_file,
            processor=processor
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
            BRUTE_FORCE_ALERT
        )

        suspicious_success_alerts = self.analyser.detection_engine.get_alert_count(
            SUSPICIOUS_SUCCESS_ALERT
        )

        user_targeting_alerts = self.analyser.detection_engine.get_alert_count(
            USER_TARGETING_ALERT
        )

        print_section_header(            
            "Live Monitoring Summary",
            Fore.GREEN
        )

        brute_force_colour = get_live_status_colour("brute_force_alert", brute_force_alerts)

        suspicious_colour = get_live_status_colour("suspicious_success", suspicious_success_alerts)
        
        user_targeting_colour = get_live_status_colour("user_targeting", user_targeting_alerts)

        processor.print_live_stats()

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