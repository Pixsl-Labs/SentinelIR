"""
File menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


def build_file_menu(window) -> None:
    """
    Builds the File menu.

    Adds file-level actions such as opening log files, opening configuration files,
    saving configuration, exporting reports, and exiting the application.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """

    file_menu = window.menuBar().addMenu(
        "&File"
    )

    open_log_action = create_action(
        window=window,
        text="Open Log File",
        icon_name="log_file.png",
        callback=open_log_file,
        shortcut="Ctrl+O"
    )

    file_menu.addAction(
        open_log_action
    )

    open_config_action = create_action(
        window=window,
        text="Open Config File",
        icon_name="config_file.png",
        callback=open_config_file,
        shortcut="Ctrl+Shift+O"
    )

    file_menu.addAction(
        open_config_action
    )

    file_menu.addSeparator()

    save_config_action = create_action(
        window=window,
        text="Save Config",
        icon_name="save_config.png",
        callback=save_config,
        shortcut="Ctrl+S"
    )

    file_menu.addAction(
        save_config_action
    )

    file_menu.addSeparator()

    export_report_action = create_action(
        window=window,
        text="Export Report",
        icon_name="export_report.png",
        callback=export_report,
        shortcut="Ctrl+E"
    )

    file_menu.addAction(
        export_report_action
    )

    file_menu.addSeparator()

    exit_action = create_action(
        window=window,
        text="Exit",
        icon_name="exit.png",
        callback=exit_application,
        shortcut="Ctrl+Q"
    )

    file_menu.addAction(
        exit_action
    )

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
