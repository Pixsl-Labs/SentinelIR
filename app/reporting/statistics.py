from app.log_analyser.log_entry import LogEntry
from app.log_analyser.filtering import LogFilter


from app.utils.formatting import (
    print_table_header,
    format_column, 
    format_service_column,
    format_status_code_column,
    format_user_column
)
from app.utils.severity import get_severity_level
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count,
    print_generated_timestamp,
    print_stat_row
)
from app.utils.colours import (
    get_severity_colour, 
    get_attempt_colour,
    get_count_colour
)


from app.models.statistics_results import (
    TargetedUserResult,
    FailedLoginSummaryResult
)
from app.detection.detection_engine import DetectionEngine


from datetime import time, datetime
from colorama import Fore


class Statistics:
    """
    Provides statistics and summary reporting methods.

    This mixin returns and prints failed login statistics, successful login
    statistics, targeted user summaries, attack statistics, and condensed analysis
    summaries.
    """
    def get_failed_logins(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            status: str | None=None,
            service: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None,
            method: str | None=None,
            path:  str | None=None,
            status_code: int | None=None
        ) -> list[LogEntry]:
        """
        Returns filtered failed login attempts.

        Applies optional filters to failed login entries and returns matching results
        sorted by timestamp.

        Args:
            ip (str | None): IP address to match.
                Defaults to None.
            username (str | None): Username to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.
            status (str | None): Login status to match.
                Defaults to None.
            start_time (time | None): Earliest event time to include.
                Defaults to None.
            end_time (time | None): Latest event time to include.
                Defaults to None.

        Returns:
            list[LogEntry]: Filtered failed login entries sorted by timestamp.
        """

        results = LogFilter.apply_filters(
            self.analyser.failed_logins,
            ip=ip,
            username=username,
            severity=severity,
            service=service,
            status=status,
            method=method,
            path=path,
            status_code=status_code,
            start_time=start_time,
            end_time=end_time
        )

        return sorted(
            results,
            key=lambda entry: entry.timestamp or datetime.min
        )
    
    def get_failed_login_summary(
            self
        ) -> list[FailedLoginSummaryResult]:
        """
        Returns failed login results grouped by username and IP address.

        Groups failed login entries by username and source IP address, counts attempts
        for each pair, calculates severity, source service, and returns the results 
        sorted by attempt count.

        Returns:
            list[FailedLoginSummaryResult]: Grouped failed login summary results.
        """

        grouped_results = {}

        for entry in self.analyser.failed_logins:

            key = (
                entry.service,
                entry.user,
                entry.ip
            )

            grouped_results[key] = (
                grouped_results.get(key, 0) + 1
            )

        results = []

        for (
            service,
            username,
            ip
        ), attempts in grouped_results.items():
            
            severity = get_severity_level(attempts)

            results.append(
                FailedLoginSummaryResult(
                    service=service,
                    username=username,
                    ip=ip,
                    attempts=attempts,
                    severity=severity
                )
            )

        return sorted(
            results,
            key=lambda result: result.attempts,
            reverse=True
        )
    
    def print_failed_logins(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            status: str | None=None,
            service: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None,
            method: str | None=None,
            path:  str | None=None,
            status_code: int | None=None
        ) -> None:
        """
        Prints filtered failed login attempts.

        Displays failed login entries matching the selected filters in a formatted
        table, including severity, username, and IP address.

        Args:
            ip (str | None): IP address to match.
                Defaults to None.
            username (str | None): Username to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.
            status (str | None): Login status to match.
                Defaults to None.
            start_time (time | None): Earliest event time to include.
                Defaults to None.
            end_time (time | None): Latest event time to include.
                Defaults to None.

        Returns:
            None
        """

        results = self.get_failed_logins(
            ip=ip,
            username=username,
            severity=severity,
            service=service,
            status=status,
            method=method,
            path=path,
            status_code=status_code,
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

        print_generated_timestamp()

        attempt_colour = get_count_colour(len(results))

        print_total_count(
            "Total Results",
            len(results),
            attempt_colour
        )

        columns = [
            ("Service", 12),
            ("User", 12),
            ("IP Address", 16),
            ("Method", 8, "^"),
            ("Path", 24, "^"),
            ("Code", 8, "^"),
            ("Severity", 12, "^")
        ]

        print_table_header(columns)

        for entry in results:

            severity_colour = get_severity_colour(
                entry.severity
            )

            display_method = entry.method or "-"

            display_path = entry.path or "-"

            display_status_code = (
                entry.status_code
                if entry.status_code is not None
                else "-"
            )

            severity_colour = get_severity_colour(
                entry.severity
            )

            print(
                "    "
                + format_service_column(entry.service, 10)
                + format_user_column(entry.user, 12)
                + Fore.YELLOW
                + format_column(entry.ip, 16)
                + format_column(display_method, 8, "^")
                + format_column(display_path, 24, "^")
                + format_column(display_status_code, 8, "^")
                + severity_colour
                + format_status_code_column(entry.severity, 12, "^")
                + Fore.RESET
            )

    def print_failed_logins_summary(
            self
        ) -> None:
        """
        Prints grouped failed login summary results.

        Displays failed login counts grouped by username and IP address, including
        attempt count and calculated severity.

        Returns:
            None
        """

        results = self.get_failed_login_summary()

        if not results:

            print_empty_message(
                "No failed login summary found."
            )

            return
        
        print_section_header(
            "Failed Login Summary",
            Fore.YELLOW
        )

        print_generated_timestamp()

        count_colour = get_count_colour(len(results))

        print_total_count(
            "Unique Failed Login Entries",
            len(results),
            count_colour
        )

        columns = [
            ("Service", 11),
            ("User", 12),
            ("IP Address", 14),
            ("Attempts", 14, "^"),
            ("Severity", 12, "^"),
        ]

        print_table_header(columns)

        for result in results:
            attempt_colour = get_attempt_colour(result.attempts)

            severity_colour = get_severity_colour(result.severity)            

            print(
                "    "
                + format_service_column(result.service, 11)
                + attempt_colour                
                + format_user_column(result.username, 12)
                + attempt_colour
                + format_column(result.ip, 14)
                + format_column(result.attempts, 14, "^")
                + severity_colour
                + format_column(result.severity, 12, "^")
                + Fore.RESET
            )

    def get_successful_logins(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            service: str | None=None,
            status: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None,
            method: str | None=None,
            path:  str | None=None,
            status_code: int | None=None
        ) -> list[LogEntry]:
        """
        Returns filtered successful login entries.

        Applies optional filters to successful login entries and returns matching
        results sorted by timestamp.

        Args:
            ip (str | None): IP address to match.
                Defaults to None.
            username (str | None): Username to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.
            status (str | None): Login status to match.
                Defaults to None.
            start_time (time | None): Earliest event time to include.
                Defaults to None.
            end_time (time | None): Latest event time to include.
                Defaults to None.

        Returns:
            list[LogEntry]: Filtered successful login entries sorted by timestamp.
        """

        results = LogFilter.apply_filters(
            self.analyser.successful_logins,
            ip=ip,
            username=username,
            severity=severity,
            service=service,
            status=status,
            method=method,
            path=path,
            status_code=status_code,
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
            service: str | None=None,
            status: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None,
            method: str | None=None,
            path:  str | None=None,
            status_code: int | None=None
        ) -> None:
        """
        Prints filtered successful login entries.

        Displays successful authentication events matching the selected filters,
        including status, timestamp, username, and IP address.

        Args:
            ip (str | None): IP address to match.
                Defaults to None.
            username (str | None): Username to match.
                Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.
            status (str | None): Login status to match.
                Defaults to None.
            start_time (time | None): Earliest event time to include.
                Defaults to None.
            end_time (time | Non): Latest event time to include.
                Defaults to None.

        Returns:
            None
        """

        results = self.get_successful_logins(
            ip=ip,
            username=username,
            severity=severity,
            service=service,
            status=status,
            method=method,
            path=path,
            status_code=status_code,
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

        print_generated_timestamp()

        print_total_count(
            "Successful Logins",
            len(results),
            Fore.CYAN
        )

        columns = [
            ("Service", 10),
            ("Status", 11, "^"),
            ("Timestamp", 26, "^"),
            ("User", 12),
            ("IP Address", 16),
            ("Method", 8, "^"),
            ("Path", 24, "^"),
            ("Code", 8, "^")
        ]

        print_table_header(columns)

        for entry in results:

            time_str = (
                entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if entry.timestamp
                else "Unknown"
            )

            display_method = entry.method or "-"

            display_path = entry.path or "-"

            display_status_code = (
                entry.status_code
                if entry.status_code is not None
                else "-"
            )

            print(
                "    "
                + format_service_column(entry.service, 10)
                + Fore.GREEN
                + format_column(f"[{entry.status}]", 11, "^")
                + format_column(time_str, 26, "^")
                + format_user_column(entry.user, 12)
                + Fore.GREEN
                + format_column(entry.ip, 16)
                + format_column(display_method, 8, "^")
                + format_column(display_path, 24, "^")
                + format_status_code_column(display_status_code, 8, "^")
                + Fore.RESET
            )

    def get_total_failed_login_attempts(self) -> int:
        """
        Returns the total number of failed login attempts.

        Adds together all failed login counts stored by IP address.

        Returns:
            int: Total number of failed login attempts.
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
        Returns the total number of suspicious IP addresses.

        Counts the unique IP addresses that have recorded failed login attempts.

        Returns:
            int: Total number of suspicious IP addresses.
        """

        return len(self.analyser.failed_ip_counts)

    def get_total_number_of_unique_ip_addresses(self) -> int:
        """
        Returns the total number of unique IP addresses.

        Combines IP addresses from failed and successful login entries, removes
        duplicates, and returns the total count.

        Returns:
            int: Total number of unique IP addresses identified.
        """

        all_ips = set()

        for entry in self.analyser.failed_logins:
            all_ips.add(entry.ip)

        for entry in self.analyser.successful_logins:
            all_ips.add(entry.ip)

        return len(all_ips)

    def get_attack_statistics(self) -> dict[str, int | str | None]:
        """
        Returns high-level attack statistics.

        Builds a service-aware summary of analysed authentication activity, including
        failed attempts, successful logins, suspicious IPs, brute-force alerts,
        targeted users, highest severity, top attacker, and most targeted user.

        Returns:
            dict[str, int | str | None]: Summary statistics for analysed log data.
        """

        targeted_users = self.get_most_targeted_users()

        total_failed = self.get_total_failed_login_attempts()

        total_successful = self.get_total_successful_logins()

        total_suspicious_ips = len(
            self.get_suspicious_ips()
        )

        brute_force_results = DetectionEngine.get_brute_force(
            self.analyser
        )

        total_brute_force = len(
            brute_force_results
        )

        failed_service_ip_counts = {}

        for entry in self.analyser.failed_logins:

            key = (
                entry.service,
                entry.ip
            )

            failed_service_ip_counts[key] = (
                failed_service_ip_counts.get(key, 0) + 1
            )

        top_attacker_entry = max(
            failed_service_ip_counts.items(),
            key=lambda item: item[1],
            default=None
        )

        if top_attacker_entry:

            (
                top_service,
                top_ip
            ), highest_attempts = top_attacker_entry

            highest_severity = get_severity_level(
                highest_attempts
            )

            top_attacker = (
                f"{top_service} {top_ip} "
                f"({highest_attempts} attempts)"
            )

        else:

            highest_severity = "NONE"

            top_attacker = None

        if targeted_users:

            top_targeted_user = targeted_users[0]

            most_targeted_user = (
                f"{top_targeted_user.service} "
                f"{top_targeted_user.username} "
                f"({top_targeted_user.attempts} attempts)"
            )

        else:

            most_targeted_user = None

        return {
            "failed_attempts": total_failed,
            "successful_logins": total_successful,
            "suspicious_ips": total_suspicious_ips,
            "brute_force_alerts": total_brute_force,
            "targeted_users": len(targeted_users),
            "highest_severity": highest_severity,
            "top_attacker": top_attacker,
            "most_targeted_user": most_targeted_user
        }
    
    def get_most_targeted_users(self) -> list[TargetedUserResult]:
        """
        Returns users sorted by failed login attempts.

        Counts failed login attempts per username, calculates severity for each user,
        and returns the results sorted from most targeted to least targeted.

        Returns:
            list[TargetedUserResult]: Targeted user results sorted by attempt count.
        """

        user_counts = {}

        for entry in self.analyser.failed_logins:

            key = (
                entry.service,
                entry.user
            )

            user_counts[key] = (
                user_counts.get(key, 0) + 1
            )

        results = []

        for (service, username), attempts in user_counts.items():

            severity = get_severity_level(attempts)

            results.append(
                TargetedUserResult(
                    service=service,
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

        Displays usernames with failed login activity, including attempt count and
        calculated severity.

        Returns:
            None
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

        print_generated_timestamp()

        attempt_colour = get_count_colour(len(sorted_users))

        print_total_count(
            "Targeted Users Detected",
            len(sorted_users),
            attempt_colour
        )

        columns = [
            ("Service", 11),
            ("User", 10),
            ("Attempts", 8, "^"),
            ("Severity", 16, "^")
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
                "    "
                + format_service_column(result.service, 11)
                + format_user_column(result.username, 10)
                + attempt_colour
                + format_column(result.attempts, 8, "^")
                + severity_colour
                + format_column(result.severity, 16, "^")
                + Fore.RESET
            )

    def print_attack_statistics(self) -> None:
        """
        Prints high-level attack statistics.

        Displays a summary of failed attempts, successful logins, suspicious IPs,
        brute-force alerts, targeted users, highest severity, top attacker, and most
        targeted user.

        Returns:
            None
        """

        stats = self.get_attack_statistics()

        print_section_header(
            "Attack Statistics",
            Fore.GREEN
        )

        print_generated_timestamp()

        rows = [
            (
                "Failed attempts",
                stats["failed_attempts"],
                get_attempt_colour(stats["failed_attempts"])
            ),
            (
                "Successful logins",
                stats["successful_logins"],
                Fore.GREEN
            ),
            (
                "Suspicious IPs",
                stats["suspicious_ips"],
                Fore.YELLOW
            ),
            (
                "Brute-force alerts",
                stats["brute_force_alerts"],
                get_attempt_colour(stats["brute_force_alerts"])
            ),
            (
                "Targeted users",
                stats["targeted_users"],
                get_attempt_colour(stats["targeted_users"])
            ),
            (
                "Highest severity",
                stats["highest_severity"],
                get_severity_colour(stats["highest_severity"])
            ),
            (
                "Top attacker",
                stats["top_attacker"],
                get_attempt_colour(stats["failed_attempts"])
            ),
            (
                "Most targeted user",
                stats["most_targeted_user"],
                get_attempt_colour(stats["targeted_users"])
            )
        ]

        for label, value, colour in rows:
            print_stat_row(
                label,
                value,
                colour
            )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )

    def print_analysis_summary(self) -> None:
        """
        Prints a condensed analysis summary.

        Displays the key totals from the analysed log file, including failed attempts,
        successful logins, suspicious IPs, and brute-force alerts.

        Returns:
            None
        """

        stats = self.get_attack_statistics()

        print_section_header(
            "Analysis Summary",
            Fore.GREEN
        )

        print_generated_timestamp()

        rows = [
            (
                "Failed attempts",
                stats["failed_attempts"],
                get_attempt_colour(stats["failed_attempts"])
            ),
            (
                "Successful logins",
                stats["successful_logins"],
                get_count_colour(stats["successful_logins"])
            ),
            (
                "Suspicious IPs",
                stats["suspicious_ips"],
                get_count_colour(stats["suspicious_ips"])
            ),
            (
                "Brute-force alerts",
                stats["brute_force_alerts"],
                get_attempt_colour(stats["brute_force_alerts"])
            )
        ]

        for label, value, colour in rows:
            print_stat_row(
                label,
                value,
                colour
            )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )