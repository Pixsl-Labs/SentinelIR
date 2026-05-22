from datetime import time, datetime
from colorama import Fore

from app.log_analyser.log_entry import LogEntry
from app.log_analyser.filtering import LogFilter
from app.utils.colours import get_status_colour, get_severity_colour
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count
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
                f"   "
                f"{status_colour}"
                f"[{entry.status:^9}] "
                f"{time_str:<20} "
                f"{entry.user:<7} "
                f"{entry.ip:<13} "
                f"{Fore.RESET}"
                f"{severity_colour}"
                f"[{entry.severity:^8}]"
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
        Returns filtered activity timeline.
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
        Prints filtered activity timeline.
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
                f"   "
                f"{status_colour}"
                f"[{entry.status:^9}] "
                f"{time_str:<20} "
                f"{entry.user:<7} "
                f"{entry.ip}"
            )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )

    def print_all_usernames(self) -> None:
        """
        Prints all unique usernames.
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
        Prints all unique IP addresses.
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