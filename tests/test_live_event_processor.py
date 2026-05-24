from app.log_analyser.log_analyser import LogAnalyser
from app.monitoring.live_event_processor import LiveEventProcessor

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

    assert len(analyser.failed_logins) == 1
    assert analyser.failed_ip_counts["192.168.1.50"] == 1


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