from datetime import time


from app.log_analyser.log_entry import LogEntry


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
        ip: str | None=None,
        username: str | None=None,
        severity: str | None=None,
        status: str | None=None,
        start_time: time | None=None,
        end_time: time | None=None
    ) -> list[LogEntry]:
        """
        Applies optional filters to a list of log entries.

        Filters can be combined to narrow results by IP address, username, severity,
        status, start time, and end time. Entries that do not match all selected
        criteria are skipped.

        Args:
            entries (list[LogEntry]): Log entries to filter.
            ip (str | None): IP address to match.
                Defaults to None.
            username (str | None): Username to match. The comparison is
                case-insensitive. Defaults to None.
            severity (str | None): Severity level to match.
                Defaults to None.
            status (str | None): Login status to match, such as FAILED
                or SUCCESS. Defaults to None.
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

            if status and entry.status != status:
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