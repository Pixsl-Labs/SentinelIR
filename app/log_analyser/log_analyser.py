from app.log_analyser.log_entry import LogEntry
from app.detection.detection_engine import DetectionEngine


from app.utils.severity import get_severity_level
from app.utils.display import print_empty_message
from app.utils.parser import (
    extract_ip,
    extract_username,
    extract_timestamp
)


import logging
from collections import defaultdict
from colorama import Fore


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

        self.detection_engine.reset_alert_state()

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

    def analyse(
            self,
            file_path: str
        ) -> bool:
        """
        Reads and processes an authentication log file.

        Scans the selected file line by line, extracts failed login events, extracts
        successful login events, and stores valid parsed entries. Missing files are
        handled safely and reported through logging.

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

                    if "failed password" in line.lower():
                        found_failed = True
                        self.extract_failed_ip(line)
                        
                    elif (
                        "accepted password" in line.lower() 
                        or "session opened" in line.lower()
                        ):

                        found_success = True
                        self.extract_successful_login(line)            

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

        This method is retained for compatability but is no longer used by the current
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

    def extract_failed_ip(
            self, 
            line: str
        ) -> None:
        """
        Extracts and stores a failed login event from a log line.

        Parses the IP address, username, and timestamp from a failed authentication
        line. Invalid lines with missing IP addresses or timestamps are skipped. Valid
        entries update the failed IP count and are stored with a calculated severity.

        Args:
            line (str): Raw failed login log line to parse.

        Returns:
            None
        """

        ip = extract_ip(line)
        
        user = extract_username(line)
        
        timestamp = extract_timestamp(line)

        if not ip:

            logging.warning(
                f"Skipping failed login line with missing IP: {line.strip()}"
            )

            return        

        if not timestamp:

            logging.warning(
                f"Skipping failed login line with missing timestamp: {line.strip()}"
            )

            return

        self.failed_ip_counts[ip] = (
            self.failed_ip_counts.get(ip, 0) + 1
        )

        attempts = self.failed_ip_counts[ip]

        severity = get_severity_level(attempts)

        self.failed_logins.append(
            LogEntry(
                ip=ip,
                user=user,
                timestamp=timestamp,
                status="FAILED",
                severity=severity
            )
        )

    def extract_successful_login(
            self,
            line: str
        ) -> None:
        """
        Extracts and stores a successful login event from a log line.

        Parses the IP address, username, and timestamp from a successful authentication
        line. Invalid lines with missing IP addresses or timestamp are skipped. Valid
        entries are stored as successful login events. 

        Args:
            line (str): Raw successful login log line to parse.

        Returns:
            None
        """

        ip = extract_ip(line)

        user = extract_username(line)

        timestamp = extract_timestamp(line)

        if not ip:

            logging.warning(
                f"Skipping successful login line with missing IP: {line.strip()}"
            )

            return
        
        if not timestamp:

            logging.warning(
                f"Skipping successful login line with missing timestamp: {line.strip()}"
            )

            return

        self.successful_logins.append(
            LogEntry(
                ip=ip,
                user=user, 
                timestamp=timestamp, 
                status="SUCCESS"
            )
        )