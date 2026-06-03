from datetime import time

from app.log_analyser.log_entry import LogEntry


def filter_log_entries(
    entries: list[LogEntry],
    ip: str | None=None,
    username: str | None=None,
    severity: str | None=None,
    status: str | None=None,
    start_time: time | None=None,
    end_time: time | None=None
) -> list[LogEntry]:
    """
    Filters log entries using optional search criteria.

    This helper applies reusable filtering logic across lists of LogEntry objects.
    Each filter is optional, allowing the caller to filter by IP address, username,
    severity, status, start time, end time, or any combination of these values.


    Args:
        entries (list[LogEntry]): Log entries to filter.
        ip (str | None): Optional IP address to match.
            Defaults to None.
        username (str | None): Optional username to match. The comparison is
        case-insensitive.
            Defaults to None.
        severity (str | None): Optional severity level to match.
            Defaults to None.
        status (str | None): Optional login status to match, such as FAILED or SUCCESS.
            Defaults to None.
        start_time (time | None): Optional earliest time to include.
            Defaults to None.
        end_time (time | None): Optional latest time to include.
            Defaults to None.

    Returns:
        list[LogEntry]: Filtered log entries matching the selected criteria.
    """

    results = entries

    if ip:
        results = [
            entry for entry in results
            if entry.ip == ip
        ]

    if username:
        results = [
            entry for entry in results
            if entry.user.lower() == username.lower()
        ]

    if severity:
        results = [
            entry for entry in results
            if entry.severity == severity
        ]

    if status:
        results = [
            entry for entry in results
            if entry.status == status
        ]

    if start_time:
        results = [
            entry for entry in results
            if entry.timestamp
            and entry.timestamp.time() >= start_time
        ]

    if end_time:
        results = [
            entry for entry in results
            if entry.timestamp
            and entry.timestamp.time() <= end_time
        ]

    return results