from app.log_analyser.log_analyser import LogAnalyser
from app.monitoring.live_event_processor import LiveEventProcessor


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