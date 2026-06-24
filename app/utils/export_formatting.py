from datetime import datetime

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
        f"{export_status_label(entry.status):<10}"
        f"{timestamp:<22}"
        f"{entry.service:<8}"
        f"{entry.user:<14}"
        f"{entry.ip:<16}"
        f"{method:<8}"
        f"{path:<26}"
        f"{status_code:<8}"
        f"{entry.severity}\n"
    )

def export_log_entry_header() -> str:
    """
    Formats the column header for exported LogEntry report rows.

    Returns:
        str: Plain-text column header and separator.
    """

    header = (
        f"{'Status':<10}"
        f"{'Timestamp':<22}"
        f"{'Service':<8}"
        f"{'User':<14}"
        f"{'IP Address':<16}"
        f"{'Method':<8}"
        f"{'Path':<26}"
        f"{'Code':<8}"
        f"{'Severity'}\n"
    )

    separator = "-" * 122 + "\n"

    return header + separator