from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD,
    BRUTE_FORCE_TIME_WINDOW,
    USER_TARGETING_THRESHOLD
)

from app.utils.formatting import (
    format_column,
    print_table_header,
    format_service_column,
    format_user_column
)
from app.utils.severity import get_severity_level
from app.utils.risk import get_risk_level
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count,
    print_generated_timestamp
)
from app.utils.colours import (
    get_severity_colour,
    get_attempt_colour,
    get_count_colour
)

from app.models.detection_results import (
    SuspiciousIPResult,
)

from app.detection.detection_engine import (
    DetectionEngine
)

from colorama import Fore
from datetime import time


class Detection:
    """
    Provides detection-focused reporting methods.

    This mixin prints and returns detection results for brute-force activity,
    suspicious IP addresses, suspicious successful logins, and distributed
    user-targeting behaviour.
    """

    def print_brute_force_results(
            self,
            threshold=BRUTE_FORCE_THRESHOLD,
            window_seconds=BRUTE_FORCE_TIME_WINDOW
        ) -> None:
        """
        Prints detected brute-force login activity.

        Runs brute-force detection using the selected threshold and time window,
        then prints the results in a formatted table. If no results are found, an empty
        message is displayed.

        Args:
            threshold (int): Failed login threshold required to trigger a
                brute-force result. Defaults to BRUTE_FORCE_THRESHOLD.
            window_seconds (int): Maximum detection time window in seconds.
                Defaults to BRUTE_FORCE_TIME_WINDOW.

        Returns:
            None
        """

        results = DetectionEngine.get_brute_force(
            self.analyser,
            threshold,
            window_seconds
        )

        if not results:
            print_empty_message(
                "No brute force activity detected."
            )

            return

        print_section_header(
            "Brute Force Detected",
            Fore.LIGHTRED_EX
        )

        print_generated_timestamp()

        attempt_colour = get_count_colour(len(results))

        print_total_count(
            "Brute-force alerts",
            len(results),
            attempt_colour
        )

        columns = [
            ("Service", 12),
            ("IP Address", 14),
            ("Attempts", 12, "^"),
            ("Time Window", 16, "^"),
            ("Severity", 10, "^"),
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = get_severity_colour(
                result.severity
            )

            attempt_colour = get_attempt_colour(
                result.attempts
            )

            print(
                "    "
                + format_service_column(result.service, 12)
                + severity_colour
                + format_column(result.ip, 14)
                + attempt_colour
                + format_column(result.attempts, 12, "^")
                + severity_colour
                + format_column(result.time_window, 16, "^")
                + format_column(result.severity, 10, "^")
                + Fore.RESET
            )

    def print_brute_force(
        self,
        threshold,
        window_seconds
    ) -> None:
        """
        Prints brute-force detection results in a simple text format.

        Runs brute-force detection and displays each result with its IP address,
        attempt count, time window, and severity.

        Args:
            threshold (int): Failed login threshold required to trigger a result.
            window_seconds (int): Maximum detection time window in seconds.

        Returns:
            None
        """
        results = DetectionEngine.get_brute_force(
            self.analyser,
            threshold,
            window_seconds
        )

        if not results:
            print_empty_message(
                "No brute force attacks found."
            )

            return

        for result in results:

            print(
                f"Service: {result.service}"
                f"IP: {result.ip}"
                f"Attempts: {result.attempts}"
                f"Window: {result.time_window}"
                f"Severity: {result.severity}"
            )

    def print_suspicious_success(self) -> None:
        """
        Prints suspicious successful login results.

        Detects successful logins from IP addresses that previously failed
        authentication and displays the results in a formatted table.

        Returns:
            None
        """

        results = DetectionEngine.get_suspicious_success(
            self.analyser
        )

        if not results:
            print_empty_message(
                "No suspicious success detected."
            )

            return

        print_section_header(
            "Success After Failure",
            Fore.YELLOW
        )

        print_generated_timestamp()

        attempt_colour = get_count_colour(
            len(results)
        )

        print_total_count(
            "Suspicious successes",
            len(results),
            attempt_colour
        )

        columns = [
            ("Service", 12),
            ("IP Address", 14),
            ("Failed Attempts", 16, "^"),
            ("Severity", 14, "^")
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = get_severity_colour(
                result.severity
            )

            attempt_colour = get_attempt_colour(
                result.attempts
            )

            print(
                "    "
                + format_service_column(result.service, 12)
                + attempt_colour
                + format_column(result.ip, 14)
                + format_column(result.attempts, 16, "^")
                + severity_colour
                + format_column(result.severity, 14, "^")
                + Fore.RESET
            )

    def print_user_targeting(
            self,
            threshold=USER_TARGETING_THRESHOLD
        ) -> None:
        """
        Prints distributed user-targeting detection results.

        Detects usernames targeted by multiple unique IP addresses and displays each
        matching result with its username, unique IP count, total attempts, and
        severity.

        Args:
            threshold (int): Number of unique IP addresses required to trigger
                a user-targeting result. Defaults to USER_TARGETING_THRESHOLD.

        Returns:
            None
        """

        results = DetectionEngine.get_user_targeting(
            self.analyser,
            threshold
        )

        if not results:
            print_empty_message(
                "No user-targeted attacks detected."
            )

            return

        print_section_header(
            "User Targeted Attacks",
            Fore.LIGHTRED_EX
        )

        print_generated_timestamp()

        attempt_colour = get_count_colour(len(results))

        print_total_count(
            "Distributed Attacks Detected",
            len(results),
            attempt_colour
        )

        columns = [
            ("Service", 12),
            ("User", 8),
            ("Unique IPs", 12, "^"),
            ("Attempts", 12, "^"),
            ("Severity", 10, "^")
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = get_severity_colour(
                result.severity
            )

            ip_colour = get_attempt_colour(
                result.unique_ips
            )

            attempt_colour = get_attempt_colour(
                result.attempts
            )

            print(
                "    "
                + format_service_column(result.service, 12)
                + format_user_column(result.username, 8)
                + ip_colour
                + format_column(result.unique_ips, 12, "^")
                + attempt_colour
                + format_column(result.attempts, 12, "^")
                + severity_colour
                + format_column(result.severity, 10, "^")
                + Fore.RESET
            )

    def get_suspicious_ips(
            self,
            service: str | None = None,
            ip: str | None = None,
            severity: str | None = None,
        ) -> list[SuspiciousIPResult]:
        """
        Returns suspicious IP results with optional filtering.

        Builds suspicious IP results from failed login entries, grouped by service and
        IP address. This keeps SSH, FTP, and HTTP activity separate in mixed-service
        reports.

        Args:
            service (str | None): Service to match, such as SSH, FTP, or HTTP.
                Defaults to None.
            ip (str | None): IP address to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.

        Returns:
            list[SuspiciousIPResult]: Suspicious IP results matching the selected
                filters.
        """

        grouped_results = {}

        for entry in self.analyser.failed_logins:

            key = (
                entry.service,
                entry.ip
            )

            grouped_results[key] = grouped_results.get(
                key,
                0
            ) + 1

        results = []

        sorted_results = sorted(
            grouped_results.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for (
            current_service,
            current_ip
        ), count in sorted_results:

            current_severity = get_severity_level(
                count
            )

            risk_status = get_risk_level(
                count
            )

            if service and current_service != service.upper():

                continue

            if ip and current_ip != ip:

                continue

            if severity and current_severity != severity.upper():

                continue

            results.append(
                SuspiciousIPResult(
                    service=current_service,
                    ip=current_ip,
                    attempts=count,
                    severity=current_severity,
                    risk_status=risk_status
                )
            )

        return results

    def print_suspicious_ips(
            self,
            service: str | None = None,
            ip: str | None = None,
            severity: str | None = None,
            start_time: time | None = None,
            end_time: time | None = None
        ) -> None:
        """
        Prints suspicious IP results.

        Displays suspicious IP addresses grouped by service and IP address, including
        attempt count, risk status, and severity. Time arguments are accepted for menu
        compatibility but are not currently applied by this method.

        Args:
            service (str | None): Service to match, such as SSH, FTP, or HTTP.
                Defaults to None.
            ip (str | None): IP address to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.
            start_time (time | None): Optional start time accepted for shared filter
                compatibility. Defaults to None.
            end_time (time | None): Optional end time accepted for shared filter
                compatibility. Defaults to None.

        Returns:
            None
        """

        results = self.get_suspicious_ips(
            service=service,
            ip=ip,
            severity=severity
        )

        if not results:
            print_empty_message(
                "No suspicious IPs found."
            )

            return

        print_section_header(
            "Suspicious IPs (Failed Attempts)",
            Fore.YELLOW
        )

        print_generated_timestamp()

        attempt_colour = get_count_colour(
            len(results)
        )

        print_total_count(
            "Suspicious IPs Detected",
            len(results),
            attempt_colour
        )

        columns = [
            ("Service", 12),
            ("IP Address", 15),
            ("Attempts", 12, "^"),
            ("Status", 20, "^"),
            ("Severity", 12, "^")
        ]

        print_table_header(
            columns
        )

        for result in results:

            severity_colour = get_severity_colour(
                result.severity
            )

            attempt_colour = get_attempt_colour(
                result.attempts
            )

            print(
                "    "
                + format_service_column(result.service, 12)
                + attempt_colour
                + format_column(result.ip, 15)
                + format_column(result.attempts, 12, "^")
                + format_column(result.risk_status, 20, "^")
                + severity_colour
                + format_column(result.severity, 12, "^")
                + Fore.RESET
            )

    def print_anonymous_ftp_logins(self) -> None:
        """
        Prints detected anonymous FTP logins.

        Returns:
            None
        """

        results = DetectionEngine.get_anonymous_ftp_logins(
            self.analyser
        )

        if not results:

            print_empty_message(
                "No anonymous FTP logins detected."
            )

            return

        print_section_header(
            "Anonymous FTP Logins Detected",
            Fore.YELLOW
        )

        print_generated_timestamp()

        print_total_count(
            "Anonymous FTP Logins",
            len(results),
            Fore.LIGHTYELLOW_EX
        )

        columns = [
            ("IP Address", 16),
            ("Username", 14),
            ("Severity", 10)
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = get_severity_colour(
                result.severity
            )

            print(
                "    "
                + severity_colour
                + format_column(result.ip, 16)
                + format_column(result.username, 14)
                + format_column(result.severity, 10)
                + Fore.RESET
            )
