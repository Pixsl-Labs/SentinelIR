from datetime import datetime

from app.log_analyser.log_analyser import LogAnalyser

from app.parsers.parser_router import parse_log_line


def store_parsed_line(
        analyser: LogAnalyser,
        line: str
    ) -> None:
    """
    Parses a log line and stores it in the analyser if valid.

    Args:
        analyser (LogAnalyser): Log analyser instance to update.
        line (str): Raw log line to parse.

    Returns:
        None
    """

    entry = parse_log_line(
        line
    )

    if entry is None:

        return

    analyser.store_entry(
        entry
    )


def test_parse_http_line_returns_log_entry_for_failed_login() -> None:

    analyser = LogAnalyser()

    line = (
        '203.0.113.11 - - [17/Apr/2026:12:01:03 +0000] '
        '"POST /login?user=admin HTTP/1.1" 401 532'
    )

    store_parsed_line(
        analyser,
        line
    )

    assert len(analyser.failed_logins) == 1

    entry = analyser.failed_logins[0]

    assert entry.ip == "203.0.113.11"
    assert entry.user == "admin"
    assert entry.timestamp == datetime(2026, 4, 17, 12, 1, 3)
    assert entry.status == "FAILED"
    assert entry.service == "HTTP"
    assert entry.method == "POST"
    assert entry.path == "/login?user=admin"
    assert entry.status_code == 401

def test_parse_http_line_returns_log_entry_for_successful_login() -> None:

    analyser = LogAnalyser()

    line = (
        '203.0.113.10 - - [17/Apr/2026:12:00:08 +0000] '
        '"POST /login?user=guest HTTP/1.1" 200 532'
    )

    store_parsed_line(
        analyser,
        line
    )

    assert len(analyser.successful_logins) == 1

    entry = analyser.successful_logins[0]

    assert entry.ip == "203.0.113.10"
    assert entry.user == "guest"
    assert entry.timestamp == datetime(2026, 4, 17, 12, 0, 8) #"%d/%b/%Y:%H:%M:%S"
    assert entry.status == "SUCCESS"
    assert entry.service == "HTTP"
    assert entry.method == "POST"
    assert entry.path == "/login?user=guest"
    assert entry.status_code == 200

