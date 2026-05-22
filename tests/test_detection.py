from app.detection.detection_engine import DetectionEngine

from conftest import (
    brute_force_reporter,
    empty_reporter,
    distributed_reporter
)


def test_get_suspicious_ips_returns_results(
        brute_force_reporter
    ):

    results = brute_force_reporter.get_suspicious_ips()

    assert len(results) > 0


def test_get_suspicious_ips_by_ip(
        brute_force_reporter
    ):

    results = brute_force_reporter.get_suspicious_ips(
        ip="192.168.1.10"
    )

    assert len(results) > 0

    assert all(
        result.ip == "192.168.1.10"
        for result in results
    )


def test_get_suspicious_ips_by_severity(
        brute_force_reporter
    ):

    results = brute_force_reporter.get_suspicious_ips(
        severity="LOW"
    )

    assert len(results) > 0

    assert all(
        result.severity == "LOW"
        for result in results
    )


def test_get_suspicious_ips_no_results(
        empty_reporter
    ):

    results = empty_reporter.get_suspicious_ips()

    assert results == []


def test_get_bruteforce_returns_results(
        brute_force_reporter
    ):

    results = DetectionEngine.get_brute_force(brute_force_reporter.analyser, 5, 10)

    assert len(results) > 0


def test_get_bruteforce_no_results(
        empty_reporter
    ):

    results = DetectionEngine.get_brute_force(empty_reporter.analyser, 5, 10)

    assert results == []


def test_get_user_targeting_returns_results(
        distributed_reporter
    ):

    results = DetectionEngine.get_user_targeting(distributed_reporter.analyser, 5)

    assert len(results) > 0


def test_get_user_targeting_no_results(
        empty_reporter
    ):

    results = DetectionEngine.get_user_targeting(empty_reporter.analyser, 5)

    assert results == []