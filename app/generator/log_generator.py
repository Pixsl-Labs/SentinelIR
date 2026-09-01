import time


def write_lines_to_file(
        file_path: str,
        lines: list[str],
        append: bool = True
        ) -> None:
    """
    Writes generated log lines to a file.

    Uses append mode when append is True, otherwise overwrites the existing file.
    Each generated log line is written on a new line.

    Args:
        file_path (str): Path to the log file being written to.
        lines (list[str]): Generated log lines to write.
        append (bool): Whether to append to existing file.
            Defaults to True.

    Returns:
        None
    """

    mode = "a" if append else "w"

    with open(file_path, mode) as f:

        for line in lines:

            f.write(line + "\n")


def stream_lines_to_file(
        file_path: str,
        lines: list[str],
        delay_seconds: float = 0.2
        ) -> None:
    """
    Streams generated log lines into a file one at a time.

    This simulates real-time log activity while the live monitoring mode watches
    the same file. Each line is flushed immediately so it can be detected by the
    file monitor as soon as it is written.

    Args:
        file_path (str): Path to the log file being written to.
        lines (list[str]): Generated log lines to stream.
        delay_seconds (float): Delay between each written line.
            Defaults to 0.2.

    Returns:
        None
    """

    with open(file_path, "a") as file:

        for line in lines:

            file.write(line + "\n")

            file.flush()

            time.sleep(delay_seconds)
