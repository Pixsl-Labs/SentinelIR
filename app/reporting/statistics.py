from app.log_analyser.log_entry import LogEntry
from app.utils.filtering import filter_log_entries
from app.utils.colours import (
    get_severity_colour, 
    get_attempt_colour,
    get_count_colour
)
from app.utils.formatting import print_table_header, format_column
from app.utils.severity import get_severity_level
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count
)

from app.models.statistics_results import TargetedUserResult

from datetime import time, datetime
from colorama import Fore


class Statistics:
    def get_failed_logins(
        self,
        ip: str | None=None,
        username: str | None=None,
        severity: str | None=None,
        status: str | None=None,
        start_time: time | None=None,
        end_time: time | None=None
    ) -> list[LogEntry]:
        """
        Returns filtered failed login attempts.
        """

        results = filter_log_entries(
            self.analyser.failed_logins,
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        return sorted(
            results,
            key=lambda entry: entry.timestamp or datetime.min
        )
    
    def print_failed_logins(
        self,
        ip: str | None=None,
        username: str | None=None,
        severity: str | None=None,
        status: str | None=None,
        start_time: time | None=None,
        end_time: time | None=None
    ) -> None:
        """
        Prints filtered failed logins.
        """

        results = self.get_failed_logins(
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        if not results:
            print_empty_message(
                "No matching failed logins found."
            )

            return
    
        print_section_header(
            "Failed Login Results",
            Fore.YELLOW
        )

        attempt_colour = get_count_colour(len(results))

        print_total_count(
            "Total Results",
            len(results),
            attempt_colour
        )

        columns = [
            ("Severity", 12),
            ("User", 10),
            ("IP Address", 15)
        ]
        
        print_table_header(columns)

        for entry in results:

            severity_colour = (
                get_severity_colour(
                    entry.severity
                )
            )

            print(
                "   "
                + severity_colour
                + format_column(entry.severity, 12)
                + format_column(entry.user, 10)
                + format_column(entry.ip, 15)
            )

    def get_successful_logins(
        self,
        ip: str | None=None,
        username: str | None=None,
        severity: str | None=None,
        status: str | None=None,
        start_time: time | None=None,
        end_time: time | None=None
        ) -> list[LogEntry]:
        """
        Returns filtered successful logins.
        """

        results = filter_log_entries(
            self.analyser.successful_logins,
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        return sorted(
            results,
            key=lambda entry: entry.timestamp or datetime.min
        )

    def print_successful_logins(
        self,
        ip: str | None=None,
        username: str | None=None,
        severity: str | None=None,
        status: str | None=None,
        start_time: time | None=None,
        end_time: time | None=None
    ) -> None:
        """
        Prints filtered successful logins.
        """

        results = self.get_successful_logins(
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        if not results:
            print_empty_message(
                "No successful logins found."
            )

            return
        
        print_section_header(
            "Successful Logins",
            Fore.GREEN
        )

        print_total_count(
            "Successful Logins",
            len(results),
            Fore.CYAN
        )

        columns = [
            ("Status", 12),
            ("Timestamp", 21),
            ("User", 10),
            ("IP Address", 15)
        ]

        print_table_header(columns)

        for entry in results:

            time_str = (
                entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if entry.timestamp
                else "Unknown"
            )

            print(
                Fore.GREEN
                +
                "   "
                + format_column(f"[{entry.status}]", 12)
                + format_column(time_str, 21)
                + format_column(entry.user, 10)
                + format_column(entry.ip, 15)
            )

    def get_total_failed_login_attempts(self) -> int:
        """
        Returns the total number of failed logins detected

        Returns:
            int: Total number of failed login attempts
        """
        return sum(self.analyser.failed_ip_counts.values())

    def get_total_successful_logins(self) -> int:
        """
        Returns the total number of successful logins

        Returns:
            int: Total number of successful logins
        """
        return len(self.analyser.successful_logins)

    def get_total_suspicious_ips(self) -> int:
        """
        Returns the total number of suspicious IPs detected.

        Returns:
            int: Total number of suspicious IPs
        """
        return len(self.analyser.failed_ip_counts)

    def get_total_number_of_unique_ip_addresses(self) -> int:
        """
        Returns the total number of unique IP addresses detected

        Returns:
            int: Total number of unique IP addresses identified
        """
        all_ips = set()

        for entry in self.analyser.failed_logins:
            all_ips.add(entry.ip)

        for entry in self.analyser.successful_logins:
            all_ips.add(entry.ip)

        return len(all_ips)

    def get_attack_statistics(self) -> dict:
        """
        Returns a high-level summary of attack statistics.

        Returns:
            dict: Summary statistics for analysed log data
        """

        total_failed = self.get_total_failed_login_attempts()

        total_successful = self.get_total_successful_logins()

        total_suspicious_ips = self.get_total_suspicious_ips()

        total_brute_force = len(self.get_bruteforce())

        total_targeted_users = len(self.get_most_targeted_users())

        highest_severity = "NONE"

        if self.analyser.failed_ip_counts:
            highest_attempts = max(self.analyser.failed_ip_counts.values())
            highest_severity = get_severity_level(highest_attempts)

        top_attacker = None

        if self.analyser.failed_ip_counts:
            top_ip, attempts = max(
                self.analyser.failed_ip_counts.items(),
                key=lambda x: x[1]
            )

            top_attacker = f"{top_ip} ({attempts} attempts)"

        most_targeted_user = None

        targeted_users = self.get_most_targeted_users()

        if targeted_users:
            top_result = targeted_users[0]
            
            top_user = top_result.username
            attempts = top_result.attempts

            most_targeted_user = f"{top_user} ({attempts} attempts)"

        return {
            "failed_attempts": total_failed,
            "successful_logins": total_successful,
            "suspicious_ips": total_suspicious_ips,
            "brute_force_alerts": total_brute_force,
            "targeted_users": total_targeted_users,
            "highest_severity": highest_severity,
            "top_attacker": top_attacker,
            "most_targeted_user": most_targeted_user
        }
    
    def get_most_targeted_users(self) -> list[TargetedUserResult]:
        """
        Returns users sorted by failed login attempts.
        """

        user_counts = {}

        for entry in self.analyser.failed_logins:
            user_counts[entry.user] = (
                user_counts.get(entry.user, 0) + 1
            )

        results = []

        for username, attempts in user_counts.items():

            severity = get_severity_level(attempts)

            results.append(
                TargetedUserResult(
                    username=username,
                    attempts=attempts,
                    severity=severity
                )
            )

        return sorted(
            results,
            key=lambda result: result.attempts,
            reverse=True
        )

    def print_most_targeted_user(self) -> None:
        """
        Prints the most targeted users.
        """

        sorted_users = self.get_most_targeted_users()

        if not sorted_users:
            print_empty_message(
                "No targeted users found."
            )

            return

        print_section_header(
            "Most Targeted Users"
        )

        attempt_colour = get_count_colour(len(sorted_users))

        print_total_count(
            "Targeted Users Detected",
            len(sorted_users),
            attempt_colour
        )

        columns = [
            ("User", 5),
            ("Attempts", 15, "^"),
            ("Severity", 12)
        ]

        print_table_header(columns)

        for result in sorted_users:

            severity_colour = get_severity_colour(
                result.severity
            )

            attempt_colour = get_attempt_colour(
                result.attempts
            )

            print(
                "   "
                + attempt_colour
                + format_column(result.username, 5)
                + format_column(result.attempts, 15, "^")
                + severity_colour
                + format_column(result.severity, 12)
            )

    def print_attack_statistics(self) -> None:
        """
        Prints a high-level summary of detected attack statistics.
        """

        stats = self.get_attack_statistics()

        print_section_header(
            "Attack Statistics",
            Fore.GREEN
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(
            Fore.CYAN
            + f"Generated: {now}\n"
        )

        severity_colour = get_severity_colour(
            stats['highest_severity']
        )

        failed_colour = get_attempt_colour(
            stats['failed_attempts']
        )

        brute_colour = get_attempt_colour(
            stats['brute_force_alerts']
        )

        targeted_colour = get_attempt_colour(
            stats['targeted_users']
        )

        print(
            f"{'Failed attempts:':<25} "
            f"{failed_colour}"
            f"{stats['failed_attempts']}"
        )

        print(
            f"{'Successful logins:':<25} "
            f"{Fore.GREEN}"
            f"{stats['successful_logins']}"
        )

        print(
            f"{'Suspicious IPs:':<25} "
            f"{Fore.YELLOW}"
            f"{stats['suspicious_ips']}"
        )

        print(
            f"{'Brute-force alerts:':<25} "
            f"{brute_colour}"
            f"{stats['brute_force_alerts']}"
        )

        print(
            f"{'Targeted users:':<25} "
            f"{targeted_colour}"
            f"{stats['targeted_users']}"
        )
        print(
            f"{'Highest severity:':<25} "
            f"{severity_colour}"
            f"{stats['highest_severity']}"
        )
        top_attacker_colour = get_attempt_colour(
            stats['failed_attempts']
        )

        print(
            f"{'Top attacker:':<25} "
            f"{top_attacker_colour}"
            f"{stats['top_attacker']}"
        )
        most_targeted_colour = get_attempt_colour(
            stats['targeted_users']
        )

        print(
            f"{'Most targeted user:':<25} "
            f"{most_targeted_colour}"
            f"{stats['most_targeted_user']}"
        )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )

    def print_analysis_summary(self) -> None:
        """
        Prints a condensed analysis summary.
        """

        stats = self.get_attack_statistics()

        print_section_header(
            "Analysis Summary",
            Fore.GREEN
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(
            Fore.CYAN
            + f"Generated: {now}\n"
        )

        failed_colour = get_attempt_colour(
            stats['failed_attempts']
        )

        successful_colour = get_count_colour(
            stats['successful_logins']
        )

        suspicious_colour = get_count_colour(
            stats['suspicious_ips']
        )

        brute_colour = get_attempt_colour(
            stats['brute_force_alerts']
        )

        print(
            f"{'Failed attempts:':<25} "
            f"{failed_colour}"
            f"{stats['failed_attempts']}"
        )

        print(
            f"{'Successful logins:':<25} "
            f"{successful_colour}"
            f"{stats['successful_logins']}"
        )

        print(
            f"{'Suspicious IPs:':<25} "
            f"{suspicious_colour}"
            f"{stats['suspicious_ips']}"
        )

        print(
            f"{'Brute-force alerts:':<25} "
            f"{brute_colour}"
            f"{stats['brute_force_alerts']}"
        )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )