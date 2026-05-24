from colorama import Fore

from app.monitoring.file_monitor import FileMonitor
from app.monitoring.live_event_processor import LiveEventProcessor

from app.utils.display import (
    print_section_header,
    print_empty_message
)
from app.utils.colours import (
    get_live_status_colour
)

from app.detection.alert_types import (
    BRUTE_FORCE_ALERT,
    SUSPICIOUS_SUCCESS_ALERT,
    USER_TARGETING_ALERT
)


class LiveRuntime:

    def __init__(
            self,
            analyser,
            reporter,
            log_file
        ):

        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(self):

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
        Prints a live session summary when the user exits the live monitoring mode.
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

        print(f"{'Brute-force alerts:':<28} {brute_force_colour}{brute_force_alerts}")
        print(f"{'Suspicious-success alerts:':<28} {suspicious_colour}{suspicious_success_alerts}")
        print(f"{'User-targeting alerts:':<28} {user_targeting_colour}{user_targeting_alerts}")