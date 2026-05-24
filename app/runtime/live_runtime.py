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

        failed_logins = len(self.analyser.failed_logins)

        successful_logins = len(self.analyser.successful_logins)

        unique_ips = len(self.analyser.failed_ip_counts)

        alerts_raised = self.analyser.detection_engine.get_total_alerts()

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

        event_colour = get_live_status_colour("events_processed", processor.events_processed)

        failed_colour = get_live_status_colour("failed_logins", failed_logins)

        succesful_colour = get_live_status_colour("successful_logins", successful_logins)

        unique_ips_colour = get_live_status_colour("unique_ips", unique_ips)

        alerts_colour = get_live_status_colour("alerts_raised", alerts_raised)

        brute_force_colour = get_live_status_colour("brute_force_alert", brute_force_alerts)

        suspicious_colour = get_live_status_colour("suspicious_success", suspicious_success_alerts)
        
        user_targeting_colour = get_live_status_colour("user_targeting", user_targeting_alerts)

        print(f"{'Events processed:':<28} {event_colour}{processor.events_processed}")
        print(f"{'Failed logins:':<28} {failed_colour}{failed_logins}")
        print(f"{'Successful logins:':<28} {succesful_colour}{successful_logins}")
        print(f"{'Unique IPs:':<28} {unique_ips_colour}{unique_ips}")
        print(f"{'Alerts raised:':<28} {alerts_colour}{alerts_raised}")
        print(f"{'Brute-force alerts:':<28} {brute_force_colour}{brute_force_alerts}")
        print(f"{'Suspicious-success alerts:':<28} {suspicious_colour}{suspicious_success_alerts}")
        print(f"{'User-targeting alerts:':<28} {user_targeting_colour}{user_targeting_alerts}")