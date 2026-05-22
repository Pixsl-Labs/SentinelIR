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
    Analyses authentication log files to extract information about
    failed and successful login attempts.

    Tracks:
    - Failed login attempts (IP, user, timestamp)
    - Successful logins
    - Failed login counts per IP
    """

    def __init__(self):
        self.failed_logins: list[LogEntry] = []
        self.successful_logins: list[LogEntry] = []
        self.failed_ip_counts: dict[str, int] = {}

    def reset(self) -> None:
        self.failed_logins = []
        self.successful_logins = []
        self.failed_ip_counts = {}

    def group_attempts_by_ip(
        self
    ) -> dict[str, list]:
        """
        Groups failed logins timestamps by IP address.
        
        Returns:
            dict[str, list]: Dictionary mapping IP addresses
            to lists of timestamps
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
        Reads and processes a log file, extracting failed and successful
        login attempts

        Returns:
            bool: True if file was successfully processed, False otherwise
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
                        
                    elif "accepted password" in line.lower() or "session opened" in line.lower():
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
        Monitors a log file in real-time.
        """

        try:

            logging.info(
                f"Monitoring file: {file_path}"
            )

            print("\nMonitoring started...")
            print("Press CTRL+C to stop.\n")

            with open(file_path, "r") as file:

                file.seek(0, 2)

                while True:

                    line = file.readline()

                    if not line:
                        continue

                    line = line.strip()

                    print(f"[NEW LOG] {line}")

                    if "failed password" in line.lower():
                        self.extract_failed_ip(line)

                        DetectionEngine.process_live_detection()

                    elif (
                        "accepted passsword" in line.lower()
                        or "session opened" in line.lower()
                    ):
                        self.extract_successful_login(line)

                        DetectionEngine.process_live_detection()

        except FileNotFoundError:

            logging.error(
                f"Error: File '{file_path}' not found."
            )

            return False
        
        except KeyboardInterrupt:

            print_empty_message(
                "Monitoring stopped.",
                Fore.LIGHTMAGENTA_EX
            )

    def extract_failed_ip(
            self, 
            line: str
        ) -> None:
        """
        Extracts IP address, username, and timestamp from a failed login line
        and stores the result.
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
        Extracts IP address and username from a successful login line
        and stores the result.
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