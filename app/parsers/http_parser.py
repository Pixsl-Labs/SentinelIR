# HTTP Status Codes

# 200 / 201 / 204 / 302 = SUCCESS-ish
# 401 / 403 = FAILED / blocked / auth failure
# 404 = suspicious path probing later
# 500 = server error, not login failure

import re
from datetime import datetime

from app.log_analyser.log_entry import LogEntry
from app.utils.parser import extract_ip


def is_http_line(line: str) -> bool:
    """
    Checks whether a log line appears to be an HTTP access log line.

    Supports both standard HTTP access logs and SentinelIR generated HTTP logs.

    Args:
        line (str): Raw HTTP access log line to check.

    Returns:
        bool: True if the line appears to contain HTTP request data,
            otherwise False.
    """

    match = re.search(
        r'"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+\S+\s+HTTP/\d(?:\.\d)?"\s+\d{3}',
        line,
        re.IGNORECASE
    )

    return match is not None

def is_http_login(line: str) -> bool:
    """
    Checks whether an HTTP log line targets a login-related path.

    Login-related paths include common authentication or admin endpoints such as
    /login, /admin, and /wp-login.php.

    Args:
        line (str): Raw HTTP access log line to inspect.

    Returns:
        bool: True if the line appears to target a login-related path,
        otherwise False.
    """

    path = extract_http_path(line)

    if path is None:

        return False
    
    path = path.lower()


    return (
        path.startswith("/login")
        or path.startswith("/admin")
        or path.startswith("/wp")
    )

def extract_http_ip(line: str) -> str | None:
    """
    Extracts the source IP address from an HTTP access log line.

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        str | None: Extracted IP adderss, None if no IP address is found.
    """

    return extract_ip(line)

def extract_http_timestamp(line: str) -> datetime | None:
    """
    Extracts the timestamp from an HTTP access log line.

    Supports SentinelIR-style timestamps:
    Apr 17 2026 12:00:08

    Also supports access-log timestamps:
    [12/Apr/2026:12:04:10 +0000]

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        datetime | None: Parsed timestamp if available, otherwise None.
    """

    match = re.search(
        r"\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})\s+[+-]\d{4}\]",
        line
    )

    if match:

        return datetime.strptime(
            match.group(1),
            "%d/%b/%Y:%H:%M:%S"
        )

    return None

def extract_http_method(line: str) -> str | None:
    """
    Extracts the HTTP request method from an HTTP access log line.

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        str | None: HTTP method such as GET or POST, otherwise None.
    """

    match = re.search(
        r'"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+',
        line,
        re.IGNORECASE
    )

    if match:

        return match.group(1).upper()

    return None

def extract_http_path(line: str) -> str | None:
    """
    Extracts the requested URL path from an HTTP access log line.

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        str | None: Requested path such as /login or /admin, otherwise None.
    """

    match = re.search(
        r'"(?:GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(\S+)\s+HTTP/\d(?:\.\d)?"',
        line,
        re.IGNORECASE
    )

    if match:

        return match.group(1)

    return None

def extract_http_username(line: str) -> str:
    """
    Extracts a username from an HTTP access log line when available.

    Some generated or custom HTTP logs may include username information using
    patterns such as user=admin. If no username is found, unknown is returned.

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        str: Extracted username, or "unknown" if no username is found.
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

def extract_http_status_code(line: str) -> int | None:
    """
    Extracts the HTTP response status code from an HTTP access log line.

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        int | None: HTTP status code such as 200, 401, or 403,
            otherwise None.
    """

    match = re.search(
        r'"\s+(\d{3})\b',
        line
    )

    if match:

        return int(match.group(1))

    return None

def extract_http_status(line: str) -> str | None:
    """
    Converts an HTTP status code into a SentinelIR authentication status.

    Login-related 200, 201, 204, and 302 responses are treated as SUCCESS.
    401 and 403 responses are treated as FAILED. Other status codes are ignored
    for now.

    Args:
        line (str): Raw HTTP access log line.

    Returns:
        str | None: "SUCCESS", "FAILED", or None if the HTTP status code
            should not be treated as an authentication event.
    """

    status_code = extract_http_status_code(line)

    if status_code in [200, 201, 204, 302]:

        return "SUCCESS"
    
    if status_code in [401, 403]:

        return "FAILED"
    
    return None

def parse_http_line(line: str) -> LogEntry | None:
    """
    Parses a supported HTTP access log line into a LogEntry object.

    The parser extracts the source IP address, timestamp, username, HTTP method,
    request path, status code, and mapped authentication status. Lines that are
    unsupported, malformed, missing required fields, or not login-related are
    ignored safely.

    Args:
        line (str): Raw HTTP access log line to parse.

    Returns:
        LogEntry | None: Parsed HTTP LogEntry if the line is valid and relevant,
            otherwise None.
    """

    if not is_http_line(line):

        return None

    if not is_http_login(line):

        return None

    status = extract_http_status(line)

    if status is None:

        return None

    ip = extract_http_ip(line)

    if not ip:

        return None

    timestamp = extract_http_timestamp(line)

    if not timestamp:

        return None

    method = extract_http_method(line)

    if method is None:

        return None

    path = extract_http_path(line)

    if path is None:

        return None

    status_code = extract_http_status_code(line)

    if status_code is None:

        return None

    username = extract_http_username(line)

    return LogEntry(
        ip=ip,
        user=username,
        timestamp=timestamp,
        status=status,
        service="HTTP",
        method=method,
        path=path,
        status_code=status_code
    )