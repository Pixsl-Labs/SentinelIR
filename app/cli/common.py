"""
Shared helpers for SentinelIR CLI entry points
"""

import logging


from pathlib import Path
from colorama import init


from app.log_analyser.log_analyser import LogAnalyser
from app.log_analyser.log_reporter import LogReporter


from app.utils.paths import (
    APPLICATION_LOGS_DIR,
)
from app.utils.path_validation import validate_input_log_path


def initialise_cli() -> None:
    """
    Initialises shared SentinelIR CLI behaviour.
    """

    Path(APPLICATION_LOGS_DIR).mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                APPLICATION_LOGS_DIR / "application.log"
            )
        ]
    )

    init(
        autoreset=True
    )


def create_analysis_components() -> tuple[LogAnalyser, LogReporter]:
    """
    Creates a shared SentinelIR analysis object.

    Returns:
        tuple[LogAnalyser, LogReporter]: Configured analyser and reporter.
    """

    analyser = LogAnalyser()

    reporter = LogReporter(
        analyser
    )

    return analyser, reporter


def resolve_log_file(
        file_name: str
        ) -> Path:
    """
    Resolves a log filename inside the SentinelIR log directory.

    Args:
        file_name (str): Log filename supplied by the user.

    Returns:
        Path: Resolved log file path.

    Raises:
        FileNotFoundError: If the selected log file does not exist.
    """

    if not file_name.endswith(".log"):
        file_name += ".log"

    file_path = validate_input_log_path(
        file_name
    )

    if not file_path.is_file():

        raise FileNotFoundError(
            f"Log file not found: {file_path}"
        )

    return file_path


def prompts_for_log_file() -> Path:
    """
    Prompts until the user selects a valid log file.

    Returns:
        Path: Valid selected log file.
    """

    while True:

        file_name = input(
            "Enter log file name: "
        ).strip()

        try:

            return resolve_log_file(
                file_name
            )

        except FileNotFoundError as e:

            print(e)
