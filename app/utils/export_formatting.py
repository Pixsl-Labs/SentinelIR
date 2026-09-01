from datetime import datetime


EXPORT_LOG_ENTRY_COLUMNS = [
    ("service", "Service", 10, "<"),
    ("status", "Status", 11, "<"),
    ("timestamp", "Timestamp", 26, "^"),
    ("user", "User", 12, "<"),
    ("ip", "IP Address", 16, "<"),
    ("method", "Method", 8, "^"),
    ("path", "Path", 24, "^"),
    ("status_code", "Code", 8, "^"),
    ("severity", "Severity", 10, "^")
]


def export_section_header(
        title: str
        ) -> str:
    """
    Formats a plain-text section header for exported reports.

    Args:
        title (str): Section title to include in the export.

    Returns:
        str: Formatted section header string.
    """

    return f"\n=== {title} ===\n\n"


def export_generated_timestamp() -> str:
    """
    Formats a plain-text generation timestamp for exported reports.

    Returns:
        str: Formatted generation timestamp string.
    """

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return f"Generated: {now}\n\n"


def export_empty_message(
        message: str
        ) -> str:
    """
    Formats a plain-text empty-result or error-style message for exported
    reports.

    Args:
        message (str): Empty message to include in the export.

    Returns:
        str: Formatted empty message string.
    """

    return f"\n{message}"


def export_separator(
        width: int = 80
        ) -> str:
    """
    Creates a plain-text separator line for exported reports.

    Args:
        width (int): Number of separator characters.
            Defaults to 80.

    Returns:
        str: Separator string
    """

    return "-" * width + "\n"


def export_status_label(
        status: str | None
        ) -> str:
    """
    Formats an authentication status for exported reports.

    Args:
        status (str | None): Authentication status such as FAILED or SUCCESS.

    Returns:
        str: Status label string.
    """

    if not status:

        return "[UNKNOWN]"

    return f"[{status.upper()}]"


def export_missing_value(
        value
        ) -> str:
    """
    Converts missing value into a readable export placeholder.

    Args:
        value: Value to check

    Returns:
        str: Original value as text, or '-' if missing.
    """

    if value is None or value == "":

        return "-"

    return str(value)


def export_column(
        value,
        width: int,
        align: str = "<"
        ) -> str:
    """
    Formats a value into a fixed-width export column.

    Args:
        value: Value to format.
        width (int): Column width.
        align (str): Alignment direction.

    Returns:
        str: Fixed-width formatted value.
    """

    return f"{str(value):{align}{width}}"


def export_log_entry_line(
        entry
        ) -> str:
    """
    Formats a LogEntry object as one plain-text export line.

    Args:
        entry: LogEntry-style object containing service, status, timestamp, user,
            IP address, severity, method, path, and status_code fields.

    Returns:
        str: Formatted log entry line.
    """

    timestamp = (
        entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if entry.timestamp
        else "Unknown"
    )

    method = export_missing_value(
        getattr(entry, "method", None)
    )

    path = export_missing_value(
        getattr(entry, "path", None)
    )

    status_code = export_missing_value(
        getattr(entry, "status_code", None)
    )

    return (
        export_column(entry.service, 10, "<")
        + export_column(export_status_label(entry.status), 11, "<")
        + export_column(timestamp, 26, "^")
        + export_column(entry.user, 12, "<")
        + export_column(entry.ip, 16, "<")
        + export_column(method, 8, "^")
        + export_column(path, 24, "^")
        + export_column(status_code, 8, "^")
        + export_column(entry.severity, 10, "^")
        + "\n"
    )


def export_log_entry_header() -> str:
    """
    Formats the column header for exported LogEntry report rows.

    Returns:
        str: Plain-text column header and separator.
    """

    header = ""

    total_width = 0

    for (
        _field_name,
        label,
        width,
        align
    ) in EXPORT_LOG_ENTRY_COLUMNS:

        header += export_column(
            label,
            width,
            align
        )

        total_width += width

    separator = "-" * total_width

    return (
        header
        + "\n"
        + separator
        + "\n"
    )


def export_filter_summary(
        filters: dict | None
        ) -> str:
    """
    Formats applied filters for a plain-text exported report.

    Args:
        filters (dict | None): Filters applied to the exported report.

    Returns:
        str: Formatted filter summary for the TXT report.
    """

    if not filters:

        return "Filters: None\n\n"

    lines = [
        "Filters Applied:\n"
    ]

    for key, value in filters.items():

        if value is None:

            continue

        lines.append(
            f"- {key}: {value}\n"
        )

    return "".join(lines) + "\n"
