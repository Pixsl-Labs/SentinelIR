from collections import defaultdict
from colorama import Fore

from app.config import (
    MAX_ATTEMPTS,
    TIME_WINDOW_SECONDS,
    SEVERITY_LEVEL
)
from app.utils.colours import (
    get_severity_colour, 
    get_status_colour, 
    get_attempt_colour, 
    get_count_colour
)
from app.utils.formatting import format_column, print_table_header


class Detection:
    def get_risk_level(self, count: int) -> str:
        """
        Returns the risk level based on the number of attempts

        Returns:
            str: Risk level
        """
        return "Investigate" if count >= MAX_ATTEMPTS else "Low risk"

    def get_severity_level(self, count: int) -> str:
        """
        Returns the severity level based on the number of attempts.

        Args:
            count (int): Number of detected attempts.

        Returns:
            str: Severity level
        """
        if count >= SEVERITY_LEVEL["HIGH"]:
            return "HIGH"

        elif count >= SEVERITY_LEVEL["MEDIUM"]:
            return "MEDIUM"

        else:
            return "LOW"

    def get_bruteforce(
            self,
            threshold=MAX_ATTEMPTS,
            window_seconds=TIME_WINDOW_SECONDS
        ) -> list[tuple[str, int, float]]:
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
                    results.append((ip, threshold, diff))
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
            print(
                Fore.LIGHTRED_EX
                + "\nNo brute force activity detected."
            )

            return

        print(
            Fore.LIGHTRED_EX
            + "\n\n=== Brute Force Detected ===\n"
        )

        attempt_colour = get_count_colour(len(results))

        print(
            f"{attempt_colour}"
            + f"   Brute force Alerts: {len(results)}\n"
        )

        columns = [
            ("IP Address", 15),
            ("Attempts", 10, "^"),
            ("Time Window", 14, "^"),
            ("Severity", 12)
        ]

        print_table_header(columns)

        for ip, attempts, diff in results:
            
            severity = self.get_severity_level(attempts)

            severity_colour = get_severity_colour(severity)

            print(
                "   "
                + severity_colour
                + format_column(
                    f"{ip}",
                    15
                )
                + format_column(
                    f"{attempts}",
                    10,
                    "^"
                )
                + format_column(
                    f"{diff}",
                    14,
                    "^"
                )
                + format_column(
                    f"{severity}",
                    12
                )
            )

    def print_suspicious_success(self) -> None:
        """
        Detects successful logins following failed attempts.
        """

        failed_ips = {
            entry.ip
            for entry in self.analyser.failed_logins
        }

        matching_ips = {
            entry.ip
            for entry in self.analyser.successful_logins
            if entry.ip in failed_ips
        }

        if not matching_ips:
            print(
                Fore.LIGHTRED_EX
                + "\nNo suspicious success detected."
            )

            return

        print(
            Fore.YELLOW
            + "\n\n=== Success After Failure ==="
        )

        attempt_colour = get_count_colour(len(matching_ips))

        print(
            f"{attempt_colour}"
            + f"\n   Matching IPs: {len(matching_ips)}\n"
        )

        columns = [
            ("IP Address", 16),
            ("Result", 10)
        ]

        print_table_header(columns)

        for ip in sorted(matching_ips):

            print(
                "   "
                + Fore.YELLOW
                + format_column(
                    f"{ip}",
                    16
                )
                + "Success after failures"
            )

    def get_user_targeting(
            self,
            threshold=MAX_ATTEMPTS
        ):
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
                results.append(
                    (user, len(unique_ips), len(ips))
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
            print(
                Fore.LIGHTRED_EX
                + "\nNo user-targeted attacks detected."
            )

            return

        print(
            Fore.LIGHTRED_EX
            + "\n\n=== User Targeted Attacks ===\n"
        )

        attempt_colour = get_count_colour(len(results))

        print(
            f"{attempt_colour}"
            + f"   Distributed Attacks Detected: {len(results)}\n"
        )

        columns = [
            ("User", 8),
            ("Unique IPs", 15, "^"),
            ("Attempts", 12, "^"),
            ("Severity", 12, "^")
        ]

        print_table_header(columns)

        for user, unique_ips, total_attempts in results:

            severity = self.get_severity_level(unique_ips)

            severity_colour = get_severity_colour(severity)

            ip_colour = get_attempt_colour(
                unique_ips
            )

            attempt_colour = get_attempt_colour(
                total_attempts
            )

            print(
                "   "
                + format_column(
                    user,
                    8
                )
                + ip_colour
                + format_column(
                    unique_ips,
                    15,
                    "^"
                )
                + attempt_colour
                + format_column(
                    total_attempts,
                    12,
                    "^"
                )
                + severity_colour
                + severity_colour
                + format_column(
                    f"[{severity}]",
                    12,
                    "^"
                )
            )

    def get_suspicious_ips(
        self,
        ip: str | None=None,
        severity: str | None=None,
    ) -> list[tuple[str, int, str]]:
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

            current_severity = self.get_severity_level(count)

            if ip and current_ip != ip:
                continue

            if severity and current_severity != severity:
                continue

            results.append(
                (
                    current_ip,
                    count,
                    current_severity
                )
            )

        return results
    
    def print_suspicious_ips(
        self,
        ip: str | None=None,
        severity: str | None=None
    ) -> None:
        """
        Prints filtered suspicious IP addresses.
        """

        results = self.get_suspicious_ips(
            ip=ip,
            severity=severity
        )

        if not results:
            print(
                Fore.LIGHTRED_EX
                + "\nNo suspicious IPs found."
            )
            return
        
        print(
            Fore.YELLOW
            + "\n\n=== Suspicious IPs (Failed Attempts) ===\n"
        )

        attempt_colour = get_count_colour(len(results))

        print(
            f"{attempt_colour}"
            + f"   Suspicious IPs Detected: {len(results)}\n"
        )

        columns = [
            ("IP Address", 15),
            ("Attempts", 12, "^"),
            ("Status", 20, "^"),
            ("Severity", 15)
        ]

        print_table_header(columns)

        for current_ip, count, current_severity in results:

            status = self.get_risk_level(count)

            severity_colour = (
                get_severity_colour(
                    current_severity
                )
            )

            attempt_colour = get_attempt_colour(count)

            print(
                "   "                
                + f"{attempt_colour}"
                + format_column(
                    f"{current_ip}",
                    15
                )
                + format_column(
                    f"{count}",
                    12,
                    "^"
                )
                + format_column(
                    f"{status}",
                    20,
                    "^"
                )
                + f"{severity_colour}"
                + format_column(
                    f"{current_severity}",
                    15
                )
            )