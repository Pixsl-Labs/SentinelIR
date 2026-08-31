import logging
from collections import defaultdict

from app.log_analyser.log_entry import LogEntry
from app.detection.detection_engine import DetectionEngine

from app.utils.severity import get_severity_level
from app.utils.display import print_empty_message

from app.parsers.parser_router import parse_log_line


class LogAnalyser:
    """
    Analyses authentication logs and stores structured login events.

    The analyser extracts failed and successful authentication activity from log
    files, stores parsed LogEntry objects, tracks failed login counts by IP
    address, and owns the detection engine used for live alerting.
    """

    def __init__(self):
        """
        Initialises the log analyser state.

        Creates empty containers for failed logins, successful logins, failed IP
        counts, and the detection engine used during static and live analysis.

        Returns:
            None
        """
        self.failed_logins: list[LogEntry] = []
        self.successful_logins: list[LogEntry] = []
        self.failed_ip_counts: dict[str, int] = {}
        self.failed_service_ip_counts: dict[tuple[str, str], int] = {}
        self.detection_engine = DetectionEngine()

    def reset(self) -> None:
        """
        Clears all stored analysis state.

        Removes failed logins, successful logins, failed IP counts, and resets the
        detection engine alert state so the analyser can process a new file cleanly.

        Returns:
            None
        """
        self.failed_logins = []
        self.successful_logins = []
        self.failed_ip_counts = {}
        self.failed_service_ip_counts = {}

        self.detection_engine.reset_alert_state()

    def has_ftp_events(self) -> bool:
        """
        Checks whether the current analysis contains FTP events.

        Returns:
            bool: True if any failed or successful login entry came from FTP,
            otherwise False.
        """

        return any(
            entry.service == "FTP"
            for entry in self.failed_logins + self.successful_logins
        )

    def group_attempts_by_ip(
        self
    ) -> dict[str, list]:
        """
        Groups failed login timestamps by IP address.

        Builds a dictionary where each IP address maps to the timestamp of its failed
        login attempts. This supports brute-force detection across time windows.

        Returns:
            dict[str, list]: Dictionary mapping IP addresses to failed login
                timestamps.
        """

        grouped_attempts = defaultdict(list)

        for entry in self.failed_logins:
            grouped_attempts[entry.ip].append(entry.timestamp)

        return grouped_attempts

    def store_entry(self, entry: LogEntry) -> None:
        """
        Stores a parsed log entry in the correct analyser collection.

        Failed entries update failed IP count, receive a calculated severity, and
        are stored in failed_logins. Successful entries are stored in
        successful_logins.

        Args:
            entry (LogEntry): Parsed log entry returned by the parser router.

        Returns:
            None
        """

        if entry.status == "FAILED":

            self.failed_ip_counts[entry.ip] = (
                self.failed_ip_counts.get(entry.ip, 0) + 1
            )

            service_ip_key = (
                entry.service,
                entry.ip
            )

            self.failed_service_ip_counts[service_ip_key] = (
                self.failed_service_ip_counts.get(service_ip_key, 0) + 1
            )

            attempts = self.failed_service_ip_counts[service_ip_key]

            entry.severity = get_severity_level(attempts)

            self.failed_logins.append(entry)

            return

        if entry.status == "SUCCESS":

            self.successful_logins.append(entry)

            return

        logging.warning(
            f"Skipping parsed entry with unsupported status: {entry.status}"
        )

    def analyse(
            self,
            file_path: str
            ) -> bool:
        """
        Reads and processes an authentication log file.

        Each line is passed to the parser router. Supported SSH, FTP, and future
        HTTP lines are converted into LogEntry objects and stored by status.
        Unsupported or malformed lines are ignored safely.

        Args:
            file_path (str): Path to the log file being analysed.

        Returns:
            bool: True if the file was processed successfully, otherwise False.
        """

        found_failed = False

        found_success = False

        try:

            logging.info(
                f"Analysing File: {file_path}"
            )

            with open(file_path, 'r') as file:
                for line in file:

                    entry = parse_log_line(
                        line.strip()
                    )

                    if entry is None:

                        continue

                    self.store_entry(
                        entry
                    )

                    if entry.status == "FAILED":

                        found_failed = True

                    elif entry.status == "SUCCESS":

                        found_success = True

            if not found_failed:

                print_empty_message(
                    "No failed login attempts found."
                )

            if not found_success:

                print_empty_message(
                    "No successful logins found."
                )

            return True

        except FileNotFoundError:

            logging.error(
                f"Error: The file '{file_path}' was not found."
            )

            return False

    def monitor(
        self,
        file_path: str
    ) -> bool:
        """
        Handles legacy monitoring calls.

        This method is retained for compatibility but is no longer used by the current
        live monitoring workflow. Live monitoring now uses FileMonitor and
        LiveEventProcessor.

        Args:
            file_path (str): Path to the log file that would have been monitored.

        Returns:
            bool: False because this legacy method is no longer active.
        """

        print_empty_message(
            "Legacy monitor() is no longer used. Use LiveRuntime instead."
        )

        return False
