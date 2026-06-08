import json
from pathlib import Path

from app.config.config_loader import load_config_dict


def save_config_dict(
            config_path: str,
            config_data: dict
    ) -> None:
    """
    Saves raw configuration data to a JSON file.

    Args:
        config_path (str): Path to the configuration file being updated.
        config_data (dict): Raw configuration dictionary to write.

    Returns:
        None
    """

    with open(config_path, "w") as file:

        json.dump(
            config_data,
            file,
            indent=4
        )

def list_available_log_files(
            log_dir: str = "log_files"
    ) -> list[str]:
    """
    Returns available log files from the configured log directory.

    Scans the selected directory for files ending in .log and returns their paths
    as strings that can be added to the watched_files configuration list.

    Args:
        log_dir (str): Directory to search for available log files.
            Defaults to "log_files".

    Returns:
        list[str]: Sorted list of available .log file paths.
    """

    log_path = Path(log_dir)

    if not log_path.exists():

        return []
    
    return sorted(
        str(file_path)
        for file_path in log_path.glob("*.log")
        if file_path.is_file()
    )

def add_watched_file(
            config_path: str,
            file_path: str
    ) -> bool:
    """
    Adds a file path to the watched_file configuration list.

    If the file is already being watched, the configuration is left unchanged.
    Otherwise, the file path is appended to watched_files and the config file is
    saved.

    Args:
        config_path (str): Path to the SentinelIR configuration file.
        file_path (str): File path to add to watched_files.

    Returns:
        bool: True if the file was added, otherwise False if it was already present.
    """

    config_data = load_config_dict(
        config_path
    )

    watched_files = config_data.setdefault(
        "watched_files",
        []
    )

    if file_path in watched_files:

        return False
    
    watched_files.append(
        file_path
    )

    save_config_dict(
        config_path,
        config_data
    )

    return True

def remove_watched_file(
            config_path: str,
            file_path: str
    ) -> bool:
    """
    Removes a file path from the watched_files configuration list.

    The file is only removed from the SentinelIR configuration. This does not
    delete the actual log file from disk.

    Args:
        config_path (str): Path to SentinelIR configuration file.
        file_path (str): Watched file path to remove from the configuration.

    Returns:
        bool: True if the file was removed, otherwise False if it was not found.
    """

    config_data = load_config_dict(
        config_path
    )

    watched_files = config_data.setdefault(
        "watched_files",
        []
    )

    if file_path not in watched_files:

        return False
    
    watched_files.remove(
        file_path
    )

    save_config_dict(
        config_path,
        config_data
    )

    return True