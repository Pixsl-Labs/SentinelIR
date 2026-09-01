from datetime import time

from app.log_analyser.log_entry import LogEntry

from app.models.enums import (
    Service,
    AuthenticationStatus,
    Severity
)


class LogFilter:
    """
    Provides reusable filtering logic for analysed log entries.

    The LogFilter class centralises common filtering behaviour so reporting,
    statistics, and investigation features can apply the same filter rules
    consistently.
    """

    @staticmethod
    def apply_filters(
        entries: list[LogEntry],
        ip: str | None = None,
        username: str | None = None,
        severity: Severity | None = None,
        service: Service | None = None,
        status: AuthenticationStatus | None = None,
        method: str | None = None,
        path: str | None = None,
        status_code: int | None = None,
        start_time: time | None = None,
        end_time: time | None = None
    ) -> list[LogEntry]:
        """
        Applies optional filters to a list of log entries.

        Filters can be combined to narrow results by service, IP address,
        username, severity, status, HTTP method, HTTP path, HTTP status code,
        start time, and end time. Entries must match all selected filters to be
        included.

        Args:
            entries (list[LogEntry]): Log entries to filter.
            ip (str | None): IP address to match. Defaults to None.
            username (str | None): Username to match case-insensitively.
                Defaults to None.
            severity (str | None): Severity level to match, such as LOW,
                MEDIUM, or HIGH. Defaults to None.
            service (str | None): Service to match, such as SSH, FTP, or HTTP.
                Defaults to None.
            status (str | None): Authentication status to match, such as FAILED
                or SUCCESS. Defaults to None.
            method (str | None): HTTP method to match, such as GET or POST.
                Defaults to None.
            path (str | None): HTTP path or partial path to match. Defaults to None.
            status_code (int | None): HTTP status code to match. Defaults to None.
            start_time (time | None): Earliest event time to include.
                Defaults to None.
            end_time (time | None): Latest event time to include.
                Defaults to None.

        Returns:
            list[LogEntry]: Log entries matching all selected filters.
        """

        filtered_entries = []

        for entry in entries:

            if ip and entry.ip != ip:
                continue

            if username and entry.user.lower() != username.lower():
                continue

            if severity and entry.severity != severity:
                continue

            if service and entry.service != service:
                continue

            if status and entry.status != status:
                continue

            if method and (entry.method or "").upper() != method.upper():
                continue

            if path and path.lower() not in (entry.path or "").lower():
                continue

            if status_code is not None and entry.status_code != status_code:
                continue

            if (
                start_time
                and entry.timestamp
                and entry.timestamp.time() < start_time
            ):
                continue

            if (
                end_time
                and entry.timestamp
                and entry.timestamp.time() > end_time
            ):
                continue

            filtered_entries.append(entry)

        return filtered_entries
