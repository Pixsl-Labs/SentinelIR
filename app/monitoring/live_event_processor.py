from app.utils.display import (
    print_section_header,
    print_status_line
)
from app.utils.colours import get_live_status_colour
from app.parsers.parser_router import (
    parse_log_line
)

from colorama import Fore


class LiveEventProcessor:
    """
    Processes live authentication log events.

    The live event processor receives new log lines from the file monitor, updates
    the analyser state, triggers live detection checks, tracks processed events,
    and prints periodic live monitoring status updates.
    """
    def __init__(
            self,
            analyser,
            show_new_logs: bool = True,
            status_interval: int = 10
        ):
        """
        Initialises the live event processor.

        Stores the analyser, display settings, status interval, and processed event
        counter used during live monitoring.

        Args:
            analyser: Log analyser instance updated with live authentication events.
            show_new_logs (bool): Whether to print each new log line as it is processed.
                Defaults to True.
            status_interval (int): Number of processed events between live status updates.
                Defaults to 10.

        Returns:
            None
        """
        self.analyser = analyser
        self.show_new_logs = show_new_logs
        self.status_interval = status_interval
        self.events_processed = 0

    def track_processed_event(self) -> None:
        """
        Tracks processed live events.

        Increments the processed event counter and prints a live status update whenever
        the configured status interval is reached.

        Returns:
            None
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

        Identifies failed and successful authentication events, updates the analyser
        state, runs live detection checks, and tracks processed events. Irrelevant or
        empty log lines are ignored.

        Args:
            line (str): Raw log lines received from the monitored file.

        Returns:
            None
        """

        if not line:

            return

        entry = parse_log_line(line)

        if entry is None:

            return

        if self.show_new_logs:

            print(f"[NEW LOG] {line}")

        self.analyser.store_entry(
            entry
        )

        self.analyser.detection_engine.process_live_detection(
            self.analyser
        )

        self.track_processed_event()

    def print_session_activity(self) -> None:
        """
        Prints live monitoring statistics.

        Displays processed events, failed logins, successful logins, unique IP count,
        and total alerts raised during the current live monitoring session.

        Returns:
            None
        """

        stats = [
            (
                "events_processed",
                "Events processed",
                self.events_processed
            ),
            (
                "failed_logins",
                "Failed logins",
                len(self.analyser.failed_logins)
            ),
            (
                "successful_logins",
                "Successful logins",
                len(self.analyser.successful_logins)
            ),
            (
                "unique_ips",
                "Unique IPs",
                len(self.analyser.failed_ip_counts)
            ),
            (
                "alerts_raised",
                "Alerts raised",
                self.analyser.detection_engine.get_total_alerts()
            )
        ]

        for status_key, label, value in stats:

            print_status_line(
                label,
                value,
                get_live_status_colour(
                    status_key,
                    value
                )
            )

        print()

    def print_live_status(self) -> None:
        """
        Prints the live monitoring status section.

        Displays a formatted section header and then prints the current live monitoring
        statistics.

        Returns:
            None
        """

        print_section_header(
            "Live Monitoring Status",
            Fore.GREEN
        )

        self.print_session_activity()
