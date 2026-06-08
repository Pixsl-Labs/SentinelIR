from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD,
    BRUTE_FORCE_TIME_WINDOW,
    USER_TARGETING_THRESHOLD
)


from app.utils.formatting import format_column, print_table_header
from app.utils.severity import get_severity_level
from app.utils.risk import get_risk_level
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count
)
from app.utils.colours import (
    get_severity_colour,
    get_attempt_colour, 
    get_count_colour
)


from app.models.detection_results import (
    SuspiciousIPResult, 
    BruteForceResult,
    UserTargetingResult,
    SuspiciousSuccessResult
)


from app.detection.detection_engine import (
    DetectionEngine
)


from collections import defaultdict
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

        attempt_colour = get_count_colour(len(results))

        print_total_count(
            "Brute force Alerts",
            len(results),
            attempt_colour
        )

        columns = [
            ("IP Address", 15),
            ("Attempts", 10, "^"),
            ("Time Window", 14, "^"),
            ("Severity", 12)
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = get_severity_colour(result.severity)

            print(
                "   "
                + severity_colour
                + format_column(result.ip, 15)
                + format_column(result.attempts, 10, "^")
                + format_column(result.time_window, 14, "^")
                + format_column(result.severity, 12)
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

        attempt_colour = get_count_colour(
            len(results)
        )

        print_total_count(
            "Matching IPs",
            len(results),
            attempt_colour
        )

        columns = [
            ("IP Address", 16),
            ("Failed Attempts", 18, "^"),
            ("Severity", 12)
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
                "   "
                + attempt_colour
                + format_column(result.ip, 16)
                + format_column(result.attempts, 18, "^")
                + severity_colour
                + format_column(result.severity, 12)
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

        attempt_colour = get_count_colour(len(results))
        
        print_total_count(
            "Distributed Attacks Detected",
            len(results),
            attempt_colour
        )

        columns = [
            ("User", 8),
            ("Unique IPs", 15, "^"),
            ("Attempts", 12, "^"),
            ("Severity", 12, "^")
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = get_severity_colour(result.severity)

            ip_colour = get_attempt_colour(
                result.unique_ips
            )

            attempt_colour = get_attempt_colour(
                result.attempts
            )

            print(
                "   "
                + format_column(result.username, 8)
                + ip_colour
                + format_column(result.unique_ips, 15, "^")
                + attempt_colour
                + format_column(result.attempts, 12, "^")
                + severity_colour
                + format_column(result.severity, 12, "^")
            )

    def get_suspicious_ips(
            self,
            ip: str | None=None,
            severity: str | None=None,
        ) -> list[SuspiciousIPResult]:
        """
        Returns suspicious IP results with optional filtering.

        Builds suspicious IP results from failed login counts, calculates severity and
        risk status for each IP address, and optionally filters by IP address or
        severity level.

        Args:
            ip (str | None): IP address to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.

        Returns:
            list[SuspiciousIPResult]: Suspicious IP results matching the selected
            filters.
        """

        results = []

        sorted_ips = sorted(
            self.analyser.failed_ip_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for current_ip, count in sorted_ips:

            current_severity = get_severity_level(count)

            risk_status = get_risk_level(count)

            if ip and current_ip != ip:
                continue

            if severity and current_severity != severity:
                continue

            results.append(
                SuspiciousIPResult(
                    ip=current_ip,
                    attempts=count,
                    severity=current_severity,
                    risk_status=risk_status
                )
            )

        return results
    
    def print_suspicious_ips(
            self,
            ip: str | None=None,
            severity: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None
        ) -> None:
        """
        Prints suspicious IP results.

        Displays suspicious IP addresses based on failed login counts, including
        attempt count, risk status, and severity. Time arguments are accepted for menu
        compatibility but are not currently applied by this method.

        Args:
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

        attempt_colour = get_count_colour(len(results))

        print_total_count(
            "Suspicious IPs Detected",
            len(results),
            attempt_colour
        )

        columns = [
            ("IP Address", 15),
            ("Attempts", 12, "^"),
            ("Status", 20, "^"),
            ("Severity", 15)
        ]

        print_table_header(columns)

        for result in results:

            severity_colour = (
                get_severity_colour(
                    result.severity
                )
            )

            attempt_colour = get_attempt_colour(result.attempts)

            print(
                "   "
                + attempt_colour
                + format_column(result.ip, 15)
                + format_column(result.attempts, 12, "^")
                + format_column(result.risk_status, 20, "^")
                + severity_colour
                + format_column(result.severity, 15)
            )