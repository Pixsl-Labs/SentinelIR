import time


def write_lines_to_file(
        file_path: str,
        lines: list[str],
        append: bool = True
    ) -> None:
    """
    Writes generated log lines to a file.
    
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
    
    This stimulates real-time log activity while the live monitoring
    mode wathces the same file.
    
    
    Returns:
        None
    """

    with open(file_path, "a") as file:

        for line in lines:

            file.write(line + "\n")

            file.flush()

            time.sleep(delay_seconds)

if __name__ == "__main__":
    from app.generator.scenarios import generate_mixed_attack_scenario

    lines = generate_mixed_attack_scenario()

    stream_lines_to_file(
        file_path="log_files/generated.log",
        lines=lines,
        delay_seconds=0.5
    )