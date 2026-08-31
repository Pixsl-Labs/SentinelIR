from app.detection.detection_engine import DetectionEngine


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

def test_detection_engine_configure_threshold_updates_values():
    detection_engine = DetectionEngine()

    detection_engine.configure_threshold(
        brute_force_threshold=3,
        brute_force_time_window=20,
        user_targeting_threshold=4
    )

    assert detection_engine.brute_force_threshold == 3
    assert detection_engine.brute_force_time_window == 20
    assert detection_engine.user_targeting_threshold == 4
