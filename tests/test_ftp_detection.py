from app.detection.detection_engine import DetectionEngine
from app.log_analyser.log_analyser import LogAnalyser

from app.parsers.parser_router import parse_log_line


def test_anonymous_ftp_success_triggers_detection(store_parsed_line) -> None:
    
    analyser = LogAnalyser()

    line = (
        "Apr 12 2026 12:00:08 server vsftpd[2103]: "
        "FTP LOGIN SUCCESS user=anonymous ip=203.0.113.50"
    )

    store_parsed_line(
        analyser,
        line
    )

    results = DetectionEngine.get_anonymous_ftp_logins(
        analyser
    )

    assert len(results) == 1
    assert results[0].ip == "203.0.113.50"
    assert results[0].username == "anonymous"
    assert results[0].severity == "MEDIUM"


def test_normal_ftp_user_does_not_trigger_anonymous_detection(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        "Apr 12 2026 12:00:04 server vsftpd[2102]: "
        "FTP LOGIN FAILED user=admin ip=192.168.1.30"
    )

    store_parsed_line(
        analyser,
        line
    )

    results = DetectionEngine.get_anonymous_ftp_logins(
        analyser
    )

    assert len(results) == 0


def test_anonymous_ftp_failed_login_does_not_trigger_detection(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        "Apr 12 2026 12:00:16 server vsftpd[2105]: "
        "FTP LOGIN FAILED user=root ip=192.168.1.30"
    )

    store_parsed_line(
        analyser,
        line
    )

    results = DetectionEngine.get_anonymous_ftp_logins(
        analyser
    )

    assert len(results) == 0


def test_ftp_successful_login_is_parsed(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        "Apr 12 2026 12:00:12 server vsftpd[2104]: "
        "FTP LOGIN SUCCESS user=backup ip=192.168.1.40"
    )

    store_parsed_line(
        analyser,
        line
    )

    assert len(analyser.successful_logins) == 1

    entry = analyser.successful_logins[0]

    assert entry.ip == "192.168.1.40"
    assert entry.user == "backup"
    assert entry.status == "SUCCESS"
    assert entry.service == "FTP"


def test_ftp_failed_login_is_parsed(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        "Apr 12 2026 12:00:16 server vsftpd[2105]: "
        "FTP LOGIN FAILED user=root ip=192.168.1.30"
    )

    store_parsed_line(
        analyser,
        line
    )

    assert len(analyser.failed_logins) == 1

    entry = analyser.failed_logins[0]

    assert entry.ip == "192.168.1.30"
    assert entry.user == "root"
    assert entry.status == "FAILED"
    assert entry.service == "FTP"


def test_malformed_ftp_line_does_not_crash(store_parsed_line) -> None:

    analyser = LogAnalyser()

    line = (
        "BROKEN FTP LINE missing timestamp user anonymous ip unknown"
    )

    store_parsed_line(
        analyser,
        line
    )

    results = DetectionEngine.get_anonymous_ftp_logins(
        analyser
    )

    assert len(analyser.successful_logins) == 0
    assert len(analyser.failed_logins) == 0
    assert len(results) == 0