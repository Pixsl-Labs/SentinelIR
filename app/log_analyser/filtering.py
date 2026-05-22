from datetime import time

from app.log_analyser.log_entry import LogEntry


class LogFilter:

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
        Applies reusable filtering to log entries.
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