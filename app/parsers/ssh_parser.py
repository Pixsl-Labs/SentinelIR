import re

from app.log_analyser.log_entry import LogEntry
from app.utils.parser import (
    extract_ip,
    extract_timestamp
)


def is_ssh_failed_login(line: str) -> bool:
    """
    Checks whether a log line is a failed SSH login attempt.

    Args:
        line (str): Raw log line to inspect.
    Returns:
        bool: True if the line contains a failed SSH login event,
            otherwise False
    """

    return "failed password" in line.lower()

def is_ssh_successful_login(line: str) -> bool:
    """
    Checks whether a log line is a successful SSH login attempt.

    Successful SSH activity may appear as an accepted password event or a
    session opened event.

    Args:
        line (str): Raw log line to inspect.
    Returns:
        bool: True if the line contains a successful SSH login event,
            otherwise False
    """

    return ("accepted password" in line.lower()
            or "session opened" in line.lower()
    )

def is_ssh_line(line: str) -> bool:
    """
    Checks whether a log line is a relevant SSH authentication event.

    This function returns True for SSH failed login lines and SSH successful
    login lines. Irrelevant SSH/system lines are ignored.

    Args:
        line (str): Raw log line to inspect.

    Returns:
        bool: True if the line is a supported SSH authentication event,
            otherwise False.
    """

    return (
        is_ssh_failed_login(line)
        or is_ssh_successful_login(line)
    )

def extract_ssh_username(line: str) -> str:
    """
    Extracts a username from an authenticated log line.

    Supports standard SSH login formats such as:
    - Failed password for root from 192.168.1.10
    - Failed password for invalid user admin from 192.168.1.10
    - Accepted password for deploy from 192.168.1.20
    - session opened for user root

    Args:
        line (str): Raw log line to parse.

    Returns:
        str: Extracted username, or "unknown" if no username is found.
    """

    match = re.search(
        r'for (?:invalid user )?(\w+)',
        line,
        re.IGNORECASE
    )

    if match:
        
        return match.group(1)
    
    session_match = re.search(
        r"session opened for user (\W+)",
        line,
        re.IGNORECASE
    )

    if session_match:

        return session_match.group(1)

    return "unknown"

def extract_ssh_status(line: str) -> str | None:
    """
    Extracts the authentication status from an SSH log line.

    Args:
        line (str): Raw log lien to inspect.

    Returns:
        str | None: "FAILED" for failed SSH authentication,
            "SUCCESS" for successful SSH authentication, or None if
            the line is not supported SSH authentication event.
    """

    if is_ssh_failed_login:

        return "FAILED"
    
    if is_ssh_successful_login:

        return "SUCCESS"
    
    return None

def parse_ssh_line(line: str) -> LogEntry | None:
    """
    Parses a supported SSH authentication log line into a LogEntry object.

    The parser extracts the source IP address, username, timestamp, and
    authentication status. Lines missing an IP address, timestamp, or supported
    status are ignored safely.

    Args:
        line (str): Raw SSH authentication log line to parse.

    Returns:
        LogEntry | None: Parsed SSH LogEntry if the line is valid,
            otherwise None.
    """

    status = extract_ssh_status(line)

    if status is None:

        return None
    
    ip = extract_ip(line)

    if not ip:

        return None
    
    timestamp = extract_timestamp(line)

    if not timestamp:

        return None
    
    username = extract_ssh_username(line)

    return LogEntry(
        ip=ip,
        user=username,
        timestamp=timestamp,
        status=status,
        service="SSH"
    )