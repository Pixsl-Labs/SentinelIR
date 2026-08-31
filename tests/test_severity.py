from app.log_analyser.log_reporter import LogReporter
from app.utils.severity import get_severity_level

def test_high_severity():
    reporter = LogReporter(None)

    result = get_severity_level(20)

    assert result == "HIGH"

def test_medium_severity():
    reporter = LogReporter(None)

    result = get_severity_level(10)

    assert result == "MEDIUM"

def test_low_severity():
    reporter = LogReporter(None)

    result = get_severity_level(5)

    assert result == "LOW"
