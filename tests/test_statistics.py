from conftest import brute_force_reporter
import pytest

from datetime import time


@pytest.mark.parametrize(
    "filter_kwargs, validator",
    [
        (
            {"service": "HTTP"},
            lambda entry: entry.service == "HTTP"
        ),
        (
            {"ip": "203.0.113.5"},
            lambda entry: entry.ip == "203.0.113.5"
        ),
        (
            {"username": "root"},
            lambda entry: entry.user.lower() == "root"
        ),
        (
            {"severity": "LOW"},
            lambda result: result.severity == "LOW"
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

def test_get_failed_logins_filters(
        mixed_service_reporter,
        filter_kwargs,
        validator
    ):

    results = mixed_service_reporter.get_failed_logins(
        **filter_kwargs
    )

    assert len(results) > 0

    assert all(
        validator(entry)
        for entry in results
    )

def test_get_failed_logins_combined_http_filters(
        mixed_service_reporter
    ):

    results = mixed_service_reporter.get_failed_logins(
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

def test_get_failed_logins_http_filter_no_results(
            mixed_service_reporter
    ):

    results = mixed_service_reporter.get_failed_logins(
        service="HTTP",
        method="GET",
        status_code=999
    )

    assert results == []

def test_get_failed_logins_time_range(
        brute_force_reporter
    ):

    results = brute_force_reporter.get_failed_logins(
        start_time=time(12, 0, 0),
        end_time=time(12, 0, 5)
    )

    assert len(results) > 0

    assert all(
        time(12, 0, 0)
        <= entry.timestamp.time()
        <= time(12, 0, 5)
        for entry in results
    )

def test_get_failed_logins_time_range_no_results(
        brute_force_reporter
    ):

    results = brute_force_reporter.get_failed_logins(
        start_time=time(23, 0, 0),
        end_time=time(23, 5, 0)
    )

    assert results == []


@pytest.mark.parametrize(
    "filter_kwargs, validator",
    [
        (
            {"service": "HTTP"},
            lambda entry: entry.service == "HTTP"
        ),
        (
            {"ip": "192.168.2.4"},
            lambda entry: entry.ip == "192.168.2.4"
        ),
        (
            {"username": "guest"},
            lambda entry: entry.user.lower() == "guest"
        ),
        (
            {"severity": "LOW"},
            lambda entry: entry.severity == "LOW"
        ),
        (
            {"status": "SUCCESS"},
            lambda entry: entry.status == "SUCCESS"
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
            {"status_code": 200},
            lambda entry: entry.status_code == 200
        ),
    ]
)
def test_get_successful_logins_filters(
        mixed_service_reporter,
        filter_kwargs,
        validator
    ):

    results = mixed_service_reporter.get_successful_logins(
        **filter_kwargs
    )

    assert len(results) > 0

    assert all(
        validator(entry)
        for entry in results
    )

def test_get_successful_logins_combined_http_filters(
        mixed_service_reporter
    ):

    results = mixed_service_reporter.get_successful_logins(
        service="HTTP",
        status="SUCCESS",
        method="POST",
        path="/login",
        status_code=200
    )

    assert len(results) > 0

    assert all(
        entry.service == "HTTP"
        and entry.status == "SUCCESS"
        and entry.method == "POST"
        and entry.path is not None
        and "/login" in entry.path
        and entry.status_code == 200
        for entry in results
    )

def test_get_successful_logins_http_filter_no_results(
            mixed_service_reporter
    ):

    results = mixed_service_reporter.get_successful_logins(
        service="HTTP",
        method="GET",
        status_code=999
    )

    assert results == []
