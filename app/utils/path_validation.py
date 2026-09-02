from pathlib import Path


from app.utils.paths import (
    INPUT_LOGS_DIR,
    REPORTS_DIR
)


SUPPORTED_LOG_EXTENSIONS = {
    ".log"
}


SUPPORTED_REPORT_EXTENSIONS = {
    ".txt",
    ".json"
}


def validate_input_log_path(
        filename: str | Path
) -> Path:
    """
    Validates and resolves an input log file path.

    Ensures the selected file remains inside the configured input log
    directory, uses a supported log extension, exists, is a regular file,
    and can be opened for reading.

    Args:
        filename (str | Path): Log filename or path to validate.

    Returns:
        Path: Resolved and validated path to the input log file.

    Raises:
        ValueError: If the path escapes the approved log directory, uses an
            unsupported extension, or does not reference a regular file.
        FileNotFoundError: If the selected log file does not exist.
        PermissionError: If the selected log file cannot be read.
    """

    candidate = (
        INPUT_LOGS_DIR / filename
    ).resolve()

    approved_directory = INPUT_LOGS_DIR.resolve()

    if not candidate.is_relative_to(
        approved_directory
    ):

        raise ValueError(
            "Log file must be inside the configured log directory."
        )

    if candidate.suffix.lower() not in SUPPORTED_LOG_EXTENSIONS:

        raise ValueError(
            "Unsupported log file extension."
        )

    if not candidate.exists():

        raise FileNotFoundError(
            "Log file does not exist."
        )

    if not candidate.is_file():

        raise ValueError(
            "Selected log path is not a file."
        )

    try:

        with candidate.open(
            "r",
            encoding="utf-8"
        ):

            pass

    except OSError as e:

        raise PermissionError(
            "Log file caanot be read."
        ) from e

    return candidate


def validate_export_path(
        filename: str | Path
) -> Path:
    """
    Validates and resolves a report export path.

    Ensures the supplied value is a filename rather than an arbitrary path,
    uses an approved report extension, and resolves inside the configured
    reports directory.

    Args:
        filename (str | Path): Report filename to validate.

    Returns:
        Path: Resolved and validated report export path.

    Raises:
        ValueError: If the filename contains directory components, uses an
            unsupported extension, or resolves outside the reports directory.
    """

    filename = Path(
        filename
    )

    if filename.name != str(filename):

        raise ValueError(
            "Report filename must not contain directories."
        )

    if filename.suffix.lower() not in SUPPORTED_REPORT_EXTENSIONS:

        raise ValueError(
            "Report must use .txt or .json."
        )

    candidate = (
        REPORTS_DIR / filename
    ).resolve()

    approved_directory = REPORTS_DIR.resolve()

    if not candidate.is_relative_to(
        approved_directory
    ):

        raise ValueError(
            "Report must be written inside the reports directory."
        )

    return candidate
