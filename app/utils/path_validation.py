from pathlib import Path


from app.utils.paths import INPUT_LOGS_DIR


SUPPORTED_LOG_EXTENSIONS = {
    ".log"
}


def validate_input_log_path(
        filename: str | Path
) -> Path:

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
