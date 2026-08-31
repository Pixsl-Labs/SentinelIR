from datetime import time
import pytest


@pytest.mark.parametrize(
    "filter_kwargs, validator",
    [
        (
            {"service": "HTTP"},
            lambda entry: entry.service == "HTTP"
        ),
        (
            {"username": "root"},
            lambda entry: entry.user.lower() == "root"
        ),
        (
            {"status": "FAILED"},
            lambda entry: entry.status == "FAILED"
        ),
        (
            {"method": "POST"},
            lambda entry: entry.method == "POST"
        ),
        (
            {"path": "/login"},
            lambda entry: entry.path is not None and "/login" in entry.path
        ),
        (
            {"status_code": 401},
            lambda entry: entry.status_code == 401
        ),
    ]
)

def test_get_activity_timeline_filters(
        mixed_service_reporter,
        filter_kwargs,
        validator
    ):

    results = mixed_service_reporter.get_activity_timeline(
        **filter_kwargs
    )

    assert len(results) > 0

    assert all(
        validator(entry)
        for entry in results
    )

def test_get_activity_timeline_combined_http_filters(
        mixed_service_reporter
    ):

    results = mixed_service_reporter.get_activity_timeline(
        service="HTTP",
        status="FAILED",
        method="POST",
        path="/login",
        status_code=401
    )

    assert len(results) > 0

    assert all(
        entry.service == "HTTP"
        and entry.status == "FAILED"
        and entry.method == "POST"
        and entry.path is not None
        and "/login" in entry.path
        and entry.status_code == 401
        for entry in results
    )

def test_get_activity_timeline_http_filter_no_results(
            mixed_service_reporter
    ):

    results = mixed_service_reporter.get_activity_timeline(
        service="HTTP",
        method="GET",
        status_code=999
    )

    assert results == []

def test_get_activity_timeline_time_range(
        mixed_service_reporter
    ):

    start = time(12, 0, 0)
    end = time(12, 0, 5)

    results = mixed_service_reporter.get_activity_timeline(
        start_time=start,
        end_time=end
    )

    assert len(results) > 0

    assert all(
        start <= entry.timestamp.time() <= end
        for entry in results
    )


@pytest.mark.parametrize(
    "filter_kwargs, validator",
    [
        (
            {"service": "HTTP"},
            lambda result: result.service == "HTTP"
        ),
        (
            {"ip": "203.0.113.11"},
            lambda result: result.ip == "203.0.113.11"
        ),
        (
            {"severity": "LOW"},
            lambda result: result.severity == "LOW"
        )
    ]
)

def test_get_suspicious_ips_filters(
        mixed_service_reporter,
        filter_kwargs,
        validator
    ):

    results = mixed_service_reporter.get_suspicious_ips(
        **filter_kwargs
    )

    assert len(results) > 0

    assert all(
        validator(entry)
        for entry in results
    )

def test_get_suspicious_ips_combined_http_filters(
        mixed_service_reporter
    ):

    results = mixed_service_reporter.get_suspicious_ips(
        service="HTTP",
        ip="203.0.113.11",
        severity="LOW"
    )

    assert len(results) > 0

    assert all(
        result.service == "HTTP"
        and result.ip == "203.0.113.11"
        and result.severity == "LOW"
        for result in results
    )

def test_get_suspicious_ips_http_filter_no_results(
            mixed_service_reporter
    ):

    results = mixed_service_reporter.get_suspicious_ips(
        service="SMTP"
    )

    assert results == []
