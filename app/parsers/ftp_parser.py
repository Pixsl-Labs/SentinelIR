import re

from app.log_analyser.log_entry import LogEntry
from app.utils.parser import (
    extract_ip,
    extract_timestamp
)


def is_ftp_line(line: str) -> bool:
    """
    Checks whether a log line appears to be an FTP authentication line.

    Args:
        line (str): Raw log line to check.

    Returns:
        bool: True if the line appears to be FTP authentication line,
            otherwise False.
    """

    return "ftp login" in line.lower()


def is_ftp_successful_login(line: str) -> bool:
    """
    Checks whether a log line is a successful FTP login attempt.

    Args:
        line (str): Raw log line to inspect.
    Returns:
        bool: True if the line contains a successful FTP login event,
            otherwise False
    """

    return "ftp login success" in line.lower()


def is_ftp_failed_login(line: str) -> bool:
    """
    Checks whether a log line is a failed FTP login attempt.

    Args:
        line (str): Raw log line to inspect.
    Returns:
        bool: True if the line contains a failed FTP login event,
            otherwise False
    """

    return "ftp login failed" in line.lower()


def extract_ftp_status(line: str) -> str | None:
    """
    Extracts FTP authentication status from a defined FTP log line.

    Args:
        line (str): Raw FTP log line.

    Returns:
        str | None: SUCCESS, FAILED, or None if no status is found.
    """

    if is_ftp_successful_login(line):

        return "SUCCESS"

    if is_ftp_failed_login(line):

        return "FAILED"

    return None


def extract_ftp_username(line: str) -> str:
    """
    Extracts an FTP username from a defined FTP log line.

    Args:
        line (str): Raw FTP log line.

    Returns:
        str: Extracted FTP username, or "unknown" if no username is found.
    """

    match = re.search(
        r"user=([A-Za-z0-9_\-.]+)",
        line,
        re.IGNORECASE
    )

    return (
        match.group(1)
        if match
        else "unknown"
    )


def parse_ftp_line(line: str) -> LogEntry | None:
    """
    Parses a supported FTP authentication log line into a LogEntry object.

    The parser extracts the source IP address, username, timestamp, and
    authentication status. Lines missing an IP address, timestamp, or supported
    status are ignored safely.

    Args:
        line (str): Raw parse_ftp_line authentication log line to parse.

    Returns:
        LogEntry | None: Parsed parse_ftp_line LogEntry if the line is valid,
            otherwise None.
    """

    status = extract_ftp_status(line)

    if status is None:

        return None

    ip = extract_ip(line)

    if not ip:

        return None

    timestamp = extract_timestamp(line)

    if not timestamp:

        return None

    username = extract_ftp_username(line)

    return LogEntry(
        ip=ip,
        user=username,
        timestamp=timestamp,
        status=status,
        service="FTP"
    )


def is_anonymous_ftp_login(line: str) -> bool:
    """
    Checks whether a log line represents a successful anonymous FTP login.

    Args:
        line (str): Raw FTP log line to inspect.

    Returns:
        bool: True if the line is a successful FTP login using the anonymous
            username, otherwise False
    """

    return (
        extract_ftp_status(line) == "SUCCESS"
        and extract_ftp_username(line) == "anonymous"
    )
