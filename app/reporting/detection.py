from collections import defaultdict
from colorama import Fore
from datetime import time

from app.config import (
    MAX_ATTEMPTS,
    TIME_WINDOW_SECONDS
)
from app.utils.colours import (
    get_severity_colour, 
    get_status_colour, 
    get_attempt_colour, 
    get_count_colour
)
from app.utils.formatting import format_column, print_table_header
from app.utils.severity import get_severity_level
from app.utils.risk import get_risk_level
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count
)

from app.models.detection_results import (
    SuspiciousIPResult, 
    BruteForceResult,
    UserTargetingResult,
    SuspiciousSuccessResult
)


class Detection:

    def get_bruteforce(
            self,
            threshold=MAX_ATTEMPTS,
            window_seconds=TIME_WINDOW_SECONDS
        ) -> list[BruteForceResult]:
        """
        Detects brute force attacks based on failed login attempts
        within a specified time window
        """

        ip_attempts = self.analyser.group_attempts_by_ip()

        results = []

        for ip, time_stamps in ip_attempts.items():
            time_stamps.sort()

            for i in range(len(time_stamps) - threshold + 1):
                start = time_stamps[i]
                end = time_stamps[i + threshold - 1]

                diff = (end - start).total_seconds()

                if diff <= window_seconds:
                    severity = get_severity_level(threshold)

                    results.append(
                        BruteForceResult(
                            ip=ip,
                            attempts=threshold,
                            time_window=diff,
                            severity=severity
                            )
                        )
                    break

        return results

    def print_brute_force_results(
            self,
            threshold=MAX_ATTEMPTS,
            window_seconds=TIME_WINDOW_SECONDS
        ) -> None:
        """
        Prints detected brute force attacks.
        """

        results = self.get_bruteforce(
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

    def get_suspicious_success(
        self
    ) -> list[SuspiciousIPResult]:
        """
        Returns successful logins that occurred after failed login attempts.
        """

        failed_ips = {
            entry.ip
            for entry in self.analyser.failed_logins
        }

        results = []

        for entry in self.analyser.successful_logins:

            if entry.ip not in failed_ips:
                continue

            failed_attempts = sum(
                1
                for failed_entry in self.analyser.failed_logins
                if failed_entry.ip == entry.ip
            )

            severity = get_severity_level(
                failed_attempts
            )

            results.append(
                SuspiciousSuccessResult(
                    ip=entry.ip,
                    attempts=failed_attempts,
                    severity=severity
                )
            )

        return results

    def print_suspicious_success(self) -> None:
        """
        Detects successful logins following failed attempts.
        """

        results = self.get_suspicious_success()

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

    def get_user_targeting(
            self,
            threshold=MAX_ATTEMPTS
        ) -> list[UserTargetingResult]:
        """
        Detects users being targeted by multiple IPs.
        """

        user_attempts = defaultdict(list)

        for entry in self.analyser.failed_logins:
            user_attempts[entry.user].append(entry.ip)

        results = []

        for user, ips in user_attempts.items():
            unique_ips = set(ips)

            if len(unique_ips) >= threshold:
                severity = get_severity_level(len(unique_ips))

                results.append(
                    UserTargetingResult(
                        username=user, 
                        unique_ips=len(unique_ips), 
                        attempts=len(ips),
                        severity=severity)
                )

        return results

    def print_user_targeting(
            self,
            threshold=MAX_ATTEMPTS
        ) -> None:
        """
        Prints distributed user-targeting attacks.
        """

        results = self.get_user_targeting(threshold)

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
        Returns filtered suspicious IP addresses.
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
        Prints filtered suspicious IP addresses.
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