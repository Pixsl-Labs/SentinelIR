from app.utils.display import (
    print_section_header
)
from app.utils.colours import get_live_status_colour

from colorama import Fore


class LiveEventProcessor:

    def __init__(
            self,
            analyser,
            show_new_logs: bool = True,
            status_interval: int = 10
        ):
        self.analyser = analyser
        self.show_new_logs = show_new_logs
        self.status_interval = status_interval
        self.events_processed = 0

    def track_processed_event(self) -> None:
        """
        Tracks processed live events and prints periodic status updates.
        """

        self.events_processed += 1

        if self.events_processed % self.status_interval == 0:
            self.print_live_status()

    def process_line(
            self,
            line: str
        ) -> None:
        """
        Processes a single live log line.
        """

        if not line:
            return
        
        if self.show_new_logs:
            print(f"[NEW LOG] {line}")

        lower_line = line.lower()

        if "failed password" in lower_line:

            self.analyser.extract_failed_ip(
                line
            )

            self.analyser.detection_engine.process_live_detection(
                self.analyser
            )

            self.track_processed_event()

        elif (
            "accepted password" in lower_line
            or "session opened" in lower_line
        ):

            self.analyser.extract_successful_login(
                line
            )

            self.analyser.detection_engine.process_live_detection(
                self.analyser
            )

            self.track_processed_event()

    def print_live_stats(self) -> None:
        """
        Prints a lightweight live monitoring status summary.
        """

        failed_logins = len(self.analyser.failed_logins)

        successful_logins = len(self.analyser.successful_logins)

        unique_ips = len(self.analyser.failed_ip_counts)

        alerts_raised = self.analyser.detection_engine.get_total_alerts()

        event_colour = get_live_status_colour("events_processed", self.events_processed)

        failed_colour = get_live_status_colour("failed_logins", failed_logins)

        succesful_colour = get_live_status_colour("successful_logins", successful_logins)

        unique_ips_colour = get_live_status_colour("unique_ips", unique_ips)

        alerts_colour = get_live_status_colour("alerts_raised", alerts_raised)

        print(f"{'Events processed:':<25} {event_colour}{self.events_processed}")
        print(f"{'Failed logins:':<25} {failed_colour}{failed_logins}")
        print(f"{'Successful logins:':<25} {succesful_colour}{successful_logins}")
        print(f"{'Unique IPs:':<25} {unique_ips_colour}{unique_ips}")
        print(f"{'Alerts raised:':<25} {alerts_colour}{alerts_raised}\n")

    def print_live_status(self) -> None:
        """
        Prints a lightweight live monitoring status summary.
        """

        print_section_header(            
            "Live Monitoring Status",
            Fore.GREEN
        )

        self.print_live_stats()