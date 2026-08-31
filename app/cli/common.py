"""
Shared helpers for SentinelIR CLI entry points
"""

import logging

from pathlib import Path
from colorama import init

from app.log_analyser.log_analyser import LogAnalyser
from app.log_analyser.log_reporter import LogReporter


LOG_FILES_DIR = Path("log_files")


def initialise_cli() -> None:
    """
    Initialises shared SentinelIR CLI behaviour.
    """

    Path("logs").mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                "logs/application.log"
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

    file_path = LOG_FILES_DIR / file_name

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
