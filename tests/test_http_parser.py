from app.log_analyser.log_analyser import LogAnalyser

from app.parsers.parser_router import parse_log_line


def store_parsed_line(
        analyser: LogAnalyser,
        line: str
    ) -> None:
    """
    Parses a log line and stores it in the analyser if valid.

    Args:
        analyser (LogAnalyser): Log analyser instance to update.
        line (str): Raw log line to parse.

    Returns:
        None
    """

    entry = parse_log_line(
        line
    )

    if entry is None:

        return

    analyser.store_entry(
        entry
    )


def test_http_lines_are_parsed_and_stored_by_analyser() -> None:

    analyser = LogAnalyser()

    log_lines = [
        (
            "Apr 17 2026 12:00:08 server nginx[3103]: "
            "HTTP LOGIN SUCCESS user=guest ip=192.168.1.7 method=POST path=/login status=200"
        ),
        
        (
            "Apr 17 2026 12:01:00 server nginx[3110]: "
            "HTTP LOGIN FAILED user=admin ip=203.0.113.10 method=POST path=/login status=401"
        ),

        (
            "Apr 17 2026 12:04:00 server nginx[3140]: "
            "HTTP ACCESS FAILED user=unknown ip=45.33.32.156 method=GET path=/admin status=403"
        )
        ]
    
    for line in log_lines:

        store_parsed_line(
            analyser,
            line
        )

    assert len(analyser.successful_logins) == 1
    assert len(analyser.failed_logins) == 2