from datetime import datetime

from app.log_analyser.log_analyser import LogAnalyser

from app.parsers.parser_router import parse_log_line


def test_parse_http_line_returns_log_entry_for_failed_login(store_parsed_line) -> None:

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

def test_parse_http_line_returns_log_entry_for_successful_login(store_parsed_line) -> None:

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
    assert entry.timestamp == datetime(2026, 4, 17, 12, 0, 8)
    assert entry.status == "SUCCESS"
    assert entry.service == "HTTP"
    assert entry.method == "POST"
    assert entry.path == "/login?user=guest"
    assert entry.status_code == 200

def test_parse_http_line_returns_none_for_non_login_path() -> None:

    line = (
        '45.33.32.157 - - [17/Apr/2026:12:07:00 +0000] '
        '"GET /products HTTP/1.1" 200 900'
    )

    entry = parse_log_line(line)

    assert entry is None

def test_extract_http_status_ignores_404_for_now() -> None:

    line = (
        '45.33.32.158 - - [17/Apr/2026:12:08:00 +0000] '
        '"POST /login?user=admin HTTP/1.1" 404 300'
    )

    entry = parse_log_line(line)

    assert entry is None

def test_parser_router_parses_http_log_line() -> None:

    line = (
        '192.0.2.44 - - [17/Apr/2026:12:05:00 +0000] '
        '"POST /login?user=deploy HTTP/1.1" 302 400'
    )

    entry = parse_log_line(line)

    assert entry is not None
    assert entry.service == "HTTP"
    assert entry.status == "SUCCESS"
    assert entry.ip == "192.0.2.44"
    assert entry.user == "deploy"
    assert entry.method == "POST"
    assert entry.path == "/login?user=deploy"
    assert entry.status_code == 302