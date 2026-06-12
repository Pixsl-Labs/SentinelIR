"""
Parser router for SentinelIR log parsing.
"""

from app.log_analyser.log_entry import LogEntry

from app.parsers.ssh_parser import (
    is_ssh_line,
    parse_ssh_line
)
from app.parsers.ftp_parser import (
    is_ftp_line,
    parse_ftp_line
)
from app.parsers.http_parser import (
    is_http_line,
    parse_http_line
)


def identify_log_line(line: str) -> str | None:
    """
    Identifies the supported log type for a raw log line.

    The router checks known parser modules in a controlled order. FTP is checked
    before SSH because FTP log lines use a clear "FTP LOGIN" pattern, while SSH
    lines use authentication phrases such as "failed password" and 
    "accepted password".

    Args:
        line (str): Raw log line to inspect.

    Returns:
        bool | None: The detected log type, such as "FTP" or "SSH",
            otherwise None if the line is unsupported.
    """

    if not line:

        return None
    
    if is_ftp_line(line):

        return "FTP"
    
    if is_http_line(line):

        return "HTTP"
    
    if is_ssh_line(line):

        return "SSH"
    
    return None

def parse_log_line(line: str) -> LogEntry | None:
    """
    Routes a raw log line to the correct parser.

    Supported log lines are passed to their dedicated parser module. If the line
    is supported, malformed, or missing required fields, None is returned.

    Args:
        line (str): Raw log line to parse.

    Returns:
        LogEntry | None: Parsed LogEntry object if the line is valid then
            supported, otherwise None.
    """

    log_type = identify_log_line(line)

    if log_type == "FTP":

        return parse_ftp_line(line)
    
    if log_type == "HTTP":

        return parse_http_line(line)
    
    if log_type == "SSH":

        return parse_ssh_line(line)
    
    return None

def is_supported_log_line(line: str) -> bool:
    """
    Checks whether a raw log line is supported by SentinelIR parsers.

    Args:
        line (str): Raw log line to inspect.

    Returns:
        bool: True if the log line is routed to a supported parser,
            otherwise False
    """

    return identify_log_line(line) is not None