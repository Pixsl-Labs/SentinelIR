import re
import ipaddress
import logging

from datetime import datetime


def extract_ip(
    line: str
) -> str | None:
    """
    Extracts and validates an IP address from a log line.

    Searches the supplied log line for an IPv4 address pattern and validates it
    using the ipaddress module. Invalid or missing IP addresses are rejected so
    malformed log lines do not enter the analysis workflow.

    Args:
        line (str): Raw log line to search.

    Returns:
        str | None: Valid IP address if one is found, otherwise None.
    """

    match = re.search(
        r'\b\d{1,3}(?:\.\d{1,3}){3}\b',
        line
    )

    if not match:
        return None
    
    ip = match.group()

    try:
        ipaddress.ip_address(ip)
        return ip
    
    except ValueError:

        logging.warning(
            f"Invalid IP address detected: {ip}"
        )

        return None
    
def extract_username(
    line: str
) -> str:
    """
    Extracts a username from an authenticated log line.

    Searches for usernames that appear after the word "for", including standard
    and "invalid user" SSH log formats. If no username can be identified, the
    function returns "unknown".

    Args:
        line (str): Raw log line to search.

    Returns:
        str: Extracted username, or "unknown" if no username is found.
    """

    match = re.search(
        r'for (?:invalid user )?(\w+)',
        line,
        re.IGNORECASE
    )

    return (
        match.group(1)
        if match
        else "unknown"
    )

def extract_timestamp(
    line: str
) -> datetime | None:
    """
    Extracts and validates a timestamp from a log line.

    Searches for a timestamp at the start of the log line and converts it into a
    datetime object. Invalid or missing timestamps return None so malformed log
    entries can be skipped safely.

    Args:
        line (str): Raw log line to search.

    Returns:
        datetime | None: Parsed datetime object if valid, otherwise None.
    """

    match = re.search(
        r'^\w+\s+\d+\s+\d{4}\s+\d{2}:\d{2}:\d{2}',
        line
    )

    if not match:
        return None
    
    timestamp = match.group()

    try:
        return datetime.strptime(
            timestamp,
            "%b %d %Y %H:%M:%S"
        )
    
    except ValueError:

        logging.warning(
            f"Invalid timestamp detected: {timestamp}"
        )

        return None
    
def is_ftp_line(
            line: str
    ) -> bool:
    """
    Checks whether a log line appears to be an FTP authentication line.

    Args:
        line (str): Raw log line to check.

    Returns:
        bool: True if the line appears to be FTP authentication line,
            otherwise False.
    """

    return "ftp login" in line.lower()

def extract_ftp_username(
            line: str
    ) -> str:
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

def extract_ftp_status(
            line: str
    ) -> str | None:
    """
    Extracts FTP authentication status from a defined FTP log line.

    Args:
        line (str): Raw FTP log line.

    Returns:
        str | None: SUCCESS, FAILED, or None if no status is found.
    """

    lower_line = line.lower()

    if "ftp login success" in lower_line:

        return "SUCCESS"
    
    if "ftp login failed" in lower_line:

        return "FAILED"
    
    return None