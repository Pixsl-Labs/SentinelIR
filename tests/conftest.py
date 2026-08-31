import pytest

from app.log_analyser.log_analyser import LogAnalyser
from app.log_analyser.log_reporter import LogReporter

from app.parsers.parser_router import parse_log_line


@pytest.fixture
def brute_force_reporter():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/brute_force.log")
    return LogReporter(analyser)


@pytest.fixture
def clean_reporter():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/clean.log")
    return LogReporter(analyser)


@pytest.fixture
def distributed_reporter():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/distributed_attack.log")
    return LogReporter(analyser)


@pytest.fixture
def malformed_reporter():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/malformed.log")
    return LogReporter(analyser)

@pytest.fixture
def mixed_service_reporter():

    analyser = LogAnalyser()

    analyser.analyse(
        "tests/test_logs/generated.log"
    )

    return LogReporter(
        analyser
    )

@pytest.fixture
def empty_reporter():
    analyser = LogAnalyser()
    analyser.analyse("tests/test_logs/empty.log")
    return LogReporter(analyser)

@pytest.fixture
def store_parsed_line():
    """
    Returns a helper function that parses and stores a log line in an analyser.
    """

    def _store_parsed_line(
            analyser: LogAnalyser,
            line: str
        ) -> None:
        entry = parse_log_line(
            line
        )

        if entry is None:

            return

        analyser.store_entry(
            entry
        )

    return _store_parsed_line
