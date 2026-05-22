import re
import ipaddress
import logging

from datetime import datetime


def extract_ip(
    line: str
) -> str | None:
    """
    Extracts and validates an IP address from a log file.
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
    Extracts username from log line.
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
    Extracts and validates timestamp from log line.
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