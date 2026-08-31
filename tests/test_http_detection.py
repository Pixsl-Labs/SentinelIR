from datetime import datetime

from app.log_analyser.log_analyser import LogAnalyser


def test_http_failed_login_is_stored_in_failed_logins(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        '203.0.113.11 - - [17/Apr/2026:12:01:04 +0000] '
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
    assert entry.timestamp == datetime(2026, 4, 17, 12, 1, 4)  # "%d/%b/%Y:%H:%M:%S"
    assert entry.status == "FAILED"
    assert entry.service == "HTTP"
    assert entry.method == "POST"
    assert entry.path == "/login?user=admin"
    assert entry.status_code == 401


def test_http_login_keeps_method_path_and_status_code(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        '203.0.113.11 - - [17/Apr/2026:12:01:10 +0000] '
        '"POST /login?user=admin HTTP/1.1" 200 532'
    )

    store_parsed_line(
        analyser,
        line
    )

    assert len(analyser.successful_logins) == 1

    entry = analyser.successful_logins[0]

    assert entry.ip == "203.0.113.11"
    assert entry.user == "admin"
    assert entry.timestamp == datetime(2026, 4, 17, 12, 1, 10)  # "%d/%b/%Y:%H:%M:%S"
    assert entry.status == "SUCCESS"
    assert entry.service == "HTTP"
    assert entry.method == "POST"
    assert entry.path == "/login?user=admin"
    assert entry.status_code == 200
