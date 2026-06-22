from datetime import time, datetime
from colorama import Fore

from app.log_analyser.log_entry import LogEntry
from app.log_analyser.filtering import LogFilter


from app.utils.colours import (
    get_status_colour,
    get_severity_colour
)
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count,
)
from app.utils.formatting import (
    format_column,
    format_service_column,
    format_servity_column,
    format_user_column,
    print_table_header
)


class Investigation:    
    def get_suspicious_activity(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            status: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None
        ) -> list[LogEntry]:
        """
        Returns filtered suspicious activity.

        Combines failed and successful login entries, applies the selected filters, and
        returns the results sorted by timestamp.

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
            list[LogEntry]: Filtered suspicious activity sorted by timestamp.
        """

        results_ = (
            self.analyser.failed_logins
            + self.analyser.successful_logins
        )

        results = LogFilter.apply_filters(
            results_,
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
    
    def print_suspicious_activity(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            status: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None
        ) -> None:
        """
        Prints filtered suspicious activity.

        Displays failed and successful login events matching the selected filters,
        including status timestamp, username, IP address, and severity.

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

        results = self.get_suspicious_activity(
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        if not results:
            print_empty_message(
                "No matching suspicious activity found."
            )
            return
        
        print_section_header(
            "Suspicious Activity",
            Fore.GREEN
        )

        print_total_count(
            "Total Events",
            len(results),
            Fore.CYAN
        )

        columns = [
            ("Service", 10),
            ("Status", 11 ,"^"),
            ("Timestamp", 26 ,"^"),
            ("User", 12),
            ("IP Address", 16), 
            ("Status", 8)
        ]

        print_table_header(columns)

        for entry in results:

            time_str = (
                entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if entry.timestamp
                else "Unknown"
            )

            status_colour = get_status_colour(
                entry.status
            )

            severity_colour = get_severity_colour(
                entry.severity
            )

            print(
                "    "
                + format_service_column(entry.service, 10)
                + status_colour
                + format_column(f"[{entry.status}]", 11, "^")
                + format_column(time_str, 26, "^")
                + format_user_column(entry.user, 12)
                + status_colour
                + format_column(entry.ip, 16)
                + severity_colour
                + format_column(f"[{entry.severity}]", 8)
            )

    def get_activity_timeline(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            status: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None
        ) -> list[LogEntry]:
        """
        Returns a filtered activity timeline.

        Combines failed and successful login events, applies the selected filters,
        and returns matching entries in chronological order.

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
            list[LogEntry]: Filtered activity timeline sorted by timestamp.
        """

        results = (
            self.analyser.failed_logins
            + self.analyser.successful_logins
        )

        results = LogFilter.apply_filters(
            results,
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        return sorted(
            results,
            key=lambda entry: (
                entry.timestamp or datetime.min
            )
        )
    
    def print_activity_timeline(
            self,
            ip: str | None=None,
            username: str | None=None,
            severity: str | None=None,
            status: str | None=None,
            start_time: time | None=None,
            end_time: time | None=None
        ) -> None:
        """
        Prints a filtered activity timeline.

        Displays matching authentication events in chronological order, including
        status, timestamp, username, and IP address.

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

        results = self.get_activity_timeline(
            ip=ip,
            username=username,
            severity=severity,
            status=status,
            start_time=start_time,
            end_time=end_time
        )

        if not results:
            print_empty_message(
                "No matching activity timeline found."
            )
            return
        
        print_section_header(
            "Activity Timeline",
            Fore.GREEN
        )

        print_total_count(
            "Total Events",
            len(results),
            Fore.CYAN
        )

        columns = [
            ("Service", 10),
            ("Status", 11 ,"^"),
            ("Timestamp", 26 ,"^"),
            ("User", 12),
            ("IP Address", 13)
        ]

        print_table_header(columns)

        for entry in results:

            time_str = (
                entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if entry.timestamp
                else "Unknown"
            )

            status_colour = get_status_colour(
                entry.status
            )

            print(
                "    "
                + format_service_column(entry.service, 10)
                + status_colour
                + format_column(f"[{entry.status}]", 11, "^")
                + format_column(time_str, 26, "^")
                + format_user_column(entry.user, 12)
                + status_colour
                + format_column(entry.ip, 13)
            )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )

    def print_all_usernames(self) -> None:
        """
        Prints all usernames found in the activity timeline.

        Collects usernames from analysed failed and successful login events, removes
        duplicates, sorts them, and displays the available values for filtering.

        Returns:
            None
        """

        timeline = self.get_activity_timeline()

        unique_usernames = {
            entry.user
            for entry in timeline
        }

        if not unique_usernames:
            print_empty_message(
                "No usernames found."
            )

            return
        
        print_section_header(
            "All Available Users",
            Fore.GREEN
        )

        for user in sorted(unique_usernames):
            print(f"   {user}")

    def print_all_ips(self) -> None:
        """
        Prints all unique IP addresses found in the activity timeline.

        Collects IP addresses from analysed failed and successful login events, removes
        duplicates, sorts them, and displays the available values for filtering.

        Returns:
            None
        """


        timeline = self.get_activity_timeline()

        unique_ips = {
            entry.ip
            for entry in timeline
        }

        if not unique_ips:
            print_empty_message(
                "No IP addresses found."
            )

            return

        print_section_header(
            "All Available IP Addresses",
            Fore.GREEN
        )

        for ip in sorted(unique_ips):
            print(f"   {ip}")