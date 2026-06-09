"""
File menu actions for the SentinelIR GUI.
"""


def open_log_file(window) -> None:
    """
    Handles the Open Log File menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Open Log File clicked")


def open_config_file(window) -> None:
    """
    Handles the Open Config File menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Open Config File clicked")


def save_config(window) -> None:
    """
    Handles the Save Config menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Save Config clicked")


def export_report(window) -> None:
    """
    Handles the Export Report menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Export Report clicked")


def exit_application(window) -> None:
    """
    Handles the Exit menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    window.close()