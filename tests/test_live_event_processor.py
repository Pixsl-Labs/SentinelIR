from datetime import datetime

from app.log_analyser.log_analyser import LogAnalyser
from app.monitoring.live_event_processor import LiveEventProcessor
from app.detection.detection_engine import DetectionEngine

from app.detection.alert_types import (
    BRUTE_FORCE_ALERT,
    SUSPICIOUS_SUCCESS_ALERT,
    USER_TARGETING_ALERT
)


def test_live_processor_adds_failed_login():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        "Jun 10 2024 12:00:01 server sshd[123]: "
        "Failed password for root from 192.168.1.50 port 22 ssh2"
    )

    processor.process_line(line)

    entry = analyser.failed_logins[0]

    assert len(analyser.failed_logins) == 1
    assert analyser.failed_ip_counts["192.168.1.50"] == 1
    assert entry.user == "root"
    assert entry.status == "FAILED"
    assert entry.service == "SSH"


def test_live_processor_adds_successful_login():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        "Jun 10 2024 12:00:01 server sshd[123]: "
        "Accepted password for root from 192.168.1.50 port 22 ssh2"
    )

    processor.process_line(line)

    assert len(analyser.successful_logins) == 1
    assert analyser.successful_logins[0].ip == "192.168.1.50"


def test_live_processor_ignores_irrelevant_line():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = "Jun 10 2024 12:00:01 server systemd[1]: Started service"

    processor.process_line(line)

    assert len(analyser.failed_logins) == 0
    assert len(analyser.successful_logins) == 0

def test_live_brute_force_updates_alert_state():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    for i in range(1, 6):

        line = (
            f"Jun 10 2024 12:00:0{i} server sshd[123]: "
            f"Failed password for root from 192.168.70.10 port 22 ssh2"
        )

        processor.process_line(line)

    assert analyser.detection_engine.get_alert_count(BRUTE_FORCE_ALERT) == 1

def test_live_suspicious_success_updates_alert_state():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    failed_line = (
        "Jun 10 2024 12:01:01 server sshd[123]: "
        "Failed password for deploy from 192.168.70.20 port 22 ssh2"
    )

    success_line = (
        "Jun 10 2024 12:01:02 server sshd[123]: "
        "Accepted password for deploy from 192.168.70.20 port 22 ssh2"
    )

    processor.process_line(failed_line)
    processor.process_line(success_line)

    assert analyser.detection_engine.get_alert_count(SUSPICIOUS_SUCCESS_ALERT) == 1

def test_live_user_targeting_updates_alert_state():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    for i in range(1, 6):

        line = (
            f"Jun 10 2024 12:02:0{i} server sshd[123]: "
            f"Failed password for admin from 10.20.0.{i} port 22 ssh2"
        )

        processor.process_line(line)

    assert analyser.detection_engine.get_alert_count(USER_TARGETING_ALERT) == 1

def test_live_alert_suppression_prevents_duplicates():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    for i in range(1, 7):

        line = (
            "Jun 10 2024 12:03:01 server sshd[123]: "
            "Failed password for root from 192.168.70.30 port 22 ssh2"
        )

        processor.process_line(line)

    assert analyser.detection_engine.get_alert_count(BRUTE_FORCE_ALERT) == 1

def test_live_event_counter_increments():
    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    failed_line = (
        "Jun 10 2024 12:00:01 server sshd[123]: "
        "Failed password for root from 192.168.1.103 port 22 ssh2"
    )

    success_line = (
        "Jun 10 2024 12:00:02 server sshd[123]: "
        "Accepted password for root from 192.168.1.103 port 22 ssh2"
    )

    ignored_line = (
        "Jun 10 2024 12:00:03 server systemd[1]: "
        "Started Session 10 of user root"
    )

    processor.process_line(failed_line)
    processor.process_line(success_line)
    processor.process_line(ignored_line)

    assert processor.events_processed == 2

def test_live_total_alerts_count_all_alert_types():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    # Brute-force alert

    for i in range(1, 6):

        line = (
            f"Jun 10 2024 12:03:0{i} server sshd[123]: "
            f"Failed password for root from 192.168.70.30 port 22 ssh2"
        )

        processor.process_line(line)

    # Suspicious-sucess alert

    failed_line = (
        "Jun 10 2024 12:01:01 server sshd[123]: "
        "Failed password for deploy from 192.168.70.20 port 22 ssh2"
    )

    success_line = (
        "Jun 10 2024 12:01:02 server sshd[123]: "
        "Accepted password for deploy from 192.168.70.20 port 22 ssh2"
    )

    processor.process_line(failed_line)
    processor.process_line(success_line)

    # User-targeting alert

    for i in range(1, 6):

        line = (
            f"Jun 10 2024 12:02:0{i} server sshd[123]: "
            f"Failed password for admin from 10.20.0.{i} port 22 ssh2"
        )

        processor.process_line(line)

    assert analyser.detection_engine.get_total_alerts() == 3

def test_live_processor_adds_failed_ftp_login() -> None:

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    failed_line = (
        "Apr 12 2026 12:00:04 server vsftpd[2102]: "
        "FTP LOGIN FAILED user=admin ip=192.168.1.30"
    )

    processor.process_line(failed_line)

    entry = analyser.failed_logins[0]

    assert len(analyser.failed_logins) == 1
    assert analyser.failed_ip_counts["192.168.1.30"] == 1
    assert entry.user == "admin"
    assert entry.status == "FAILED"
    assert entry.service == "FTP"

def test_live_processor_adds_successful_ftp_login():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        "Apr 12 2026 12:00:12 server vsftpd[2104]: "
        "FTP LOGIN SUCCESS user=backup ip=192.168.1.40"
    )

    processor.process_line(line)

    entry = analyser.successful_logins[0]

    assert len(analyser.successful_logins) == 1
    assert entry.ip == "192.168.1.40"
    assert entry.user == "backup"
    assert entry.status == "SUCCESS"
    assert entry.service == "FTP"

def test_live_processor_processes_anonymous_ftp_login():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        "Apr 12 2026 12:00:08 server vsftpd[2103]: "
        "FTP LOGIN SUCCESS user=anonymous ip=203.0.113.50"
    )

    processor.process_line(line)

    entry = analyser.successful_logins[0]

    assert len(analyser.successful_logins) == 1
    assert entry.ip == "203.0.113.50"
    assert entry.user == "anonymous"
    assert entry.status == "SUCCESS"
    assert entry.service == "FTP"
    assert processor.events_processed == 1

def test_live_ftp_event_counter_increments():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    first_line = (
        "Apr 12 2026 12:00:08 server vsftpd[2103]: "
        "FTP LOGIN SUCCESS user=anonymous ip=203.0.113.50"
    )

    second_line = (
        "Apr 12 2026 12:00:24 server vsftpd[2107]: "
        "FTP LOGIN SUCCESS user=anonymous ip=198.51.100.77"
    )

    processor.process_line(first_line)

    assert len(analyser.successful_logins) == 1
    assert processor.events_processed == 1

    processor.process_line(second_line)

    assert len(analyser.successful_logins) == 2
    assert processor.events_processed == 2

def test_live_processor_ignores_malformed_ftp_line():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        "BROKEN FTP LINE missing timestamp user anonymous ip unknown"
    )

    processor.process_line(line)

    assert len(analyser.successful_logins) == 0
    assert len(analyser.failed_logins) == 0
    assert processor.events_processed == 0

def test_live_processor_adds_failed_http_login() -> None:

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    failed_line = (
        '203.0.113.11 - - [17/Apr/2026:12:01:01 +0000] '
        '"POST /login?user=admin HTTP/1.1" 401 532'
    )

    processor.process_line(failed_line)

    entry = analyser.failed_logins[0]

    assert len(analyser.failed_logins) == 1
    assert analyser.failed_ip_counts["203.0.113.11"] == 1
    assert entry.user == "admin"
    assert entry.status == "FAILED"
    assert entry.service == "HTTP"
    assert entry.method == "POST"
    assert entry.path == "/login?user=admin"
    assert entry.status_code == 401

def test_live_processor_adds_successful_http_login():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        '203.0.113.10 - - [17/Apr/2026:12:00:08 +0000] '
        '"POST /login?user=guest HTTP/1.1" 200 532'
    )

    processor.process_line(line)

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

def test_live_http_event_counter_increments():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    first_line = (
        '203.0.113.10 - - [17/Apr/2026:12:00:08 +0000] '
        '"POST /login?user=guest HTTP/1.1" 200 532'
    )

    second_line = (
        '203.0.113.11 - - [17/Apr/2026:12:01:10 +0000] '
        '"POST /login?user=admin HTTP/1.1" 200 532'
    )

    processor.process_line(first_line)

    assert len(analyser.successful_logins) == 1
    assert processor.events_processed == 1

    processor.process_line(second_line)

    assert len(analyser.successful_logins) == 2
    assert processor.events_processed == 2

def test_live_processor_ignores_malformed_http_line():

    analyser = LogAnalyser()

    processor = LiveEventProcessor(
        analyser=analyser,
        show_new_logs=False
    )

    line = (
        "BROKEN HTTP LINE missing timestamp user guest ip unknown"
    )

    processor.process_line(line)

    assert len(analyser.successful_logins) == 0
    assert len(analyser.failed_logins) == 0
    assert processor.events_processed == 0

def test_alert_cooldown_blocks_duplicate_alerts():
    engine = DetectionEngine()

    engine.alert_cooldown_seconds = 60

    alert_key = "SSH:192.168.70.10"

    assert engine.can_alert(
        BRUTE_FORCE_ALERT,
        alert_key,
        current_time=1000
    )

    engine.mark_alerted(
        BRUTE_FORCE_ALERT,
        alert_key,
        current_time=1000
    )

    assert not engine.can_alert(
        BRUTE_FORCE_ALERT,
        alert_key,
        current_time=1030
    )

def test_alert_count_tracks_actual_alert_events():
    engine = DetectionEngine()

    alert_key = "SSH:192.168.70.10"

    engine.mark_alerted(
        BRUTE_FORCE_ALERT,
        alert_key,
        current_time=1000
    )

    engine.mark_alerted(
        BRUTE_FORCE_ALERT,
        alert_key,
        current_time=1061
    )

    assert engine.get_alert_count(BRUTE_FORCE_ALERT) == 2
