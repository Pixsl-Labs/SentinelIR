"""
Menu bar builder for the SentinelIR GUI.
"""

from PySide6.QtGui import QAction

from app.gui.utils.icons import get_icon

from app.gui.actions.file_actions import (
    open_log_file,
    open_config_file,
    save_config,
    export_report,
    exit_application
)


def build_menu_bar(window) -> None:
    """
    Builds all GUI menus for the provided MainWindow instance.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """

    build_file_menu(window)
    build_analysis_menu(window)
    build_detection_menu(window)
    build_live_monitoring_menu(window)
    build_generator_menu(window)
    build_reports_menu(window)
    build_settings_menu(window)
    build_view_menu(window)
    build_help_menu(window)


def create_action(
        window,
        text: str,
        icon_name: str | None,
        callback,
        shortcut: str | None = None
) -> QAction:
    """
    Creates a reusable menu action.

    Builds a QAction with optional icon, optional keyboard shortcut, and a connected
    callback function. This avoids repeating QAction setup code across every menu.

    Args:
        window: MainWindow instance that owns the action.
        text (str): Text displayed for the menu action.
        icon_name (str | None): Icon filename from app/gui/assets, or None for no icon.
        callback: Function called when the action is triggered.
        shortcut (str | None): Optional keyboard shortcut, such as "Ctrl+O".
            Defaults to None.

    Returns:
        QAction: Configured menu action.
    """

    action = QAction(
        text,
        window
    )

    if icon_name is not None:

        action.setIcon(
            get_icon(icon_name)
        )

    if shortcut is not None:

        action.setShortcut(
            shortcut
        )

    action.triggered.connect(
        lambda checked=False: callback(window)
    )

    return action


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
        callback=open_config_file
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


def build_analysis_menu(window) -> None:
    """
    Builds the Analysis menu.

    This menu will contain static analysis actions such as running analysis,
    viewing summaries, viewing failed/successful logins, viewing the activity
    timeline, and clearing analysis results.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """

    analysis_menu = window.menuBar().addMenu(
        "&Analysis"
    )

    analysis_action = create_action(
        window=window,
        text="Open Log File",
        icon_name="log_file.png",
        callback=window.analysis_action,
        shortcut="Ctrl+O"
    )

    analysis_menu.addAction(
        analysis_action
    )


def build_detection_menu(window) -> None:
    """
    Builds the Detection menu.

    This menu will contain detection-focused actions such as brute-force detection,
    suspicious-success detection, user-targeting detection, suspicious IP review,
    and alert summaries.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """


def build_live_monitoring_menu(window) -> None:
    """
    Builds the Live Monitoring menu.

    This menu will contain live monitoring actions such as starting monitoring,
    stopping monitoring, selecting watched files, adding watched files, removing
    watched files, and viewing live summaries.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """


def build_generator_menu(window) -> None:
    """
    Builds the Generator menu.

    This menu will contain scenario generation actions such as generating brute-force,
    suspicious-success, user-targeting, normal activity, mixed attack scenarios, and
    streaming generated logs.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """


def build_reports_menu(window) -> None:
    """
    Builds the Reports menu.

    This menu will contain report actions such as exporting TXT reports, exporting
    JSON reports, opening the reports folder, and clearing generated reports.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """


def build_settings_menu(window) -> None:
    """
    Builds the Settings menu.

    This menu will contain configuration actions such as detection thresholds,
    live monitoring settings, watched file settings, output paths, and resetting
    defaults.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """


def build_view_menu(window) -> None:
    """
    Builds the View menu.

    This menu will contain screen navigation actions such as Dashboard, Static
    Analysis, Live Monitoring, Config, Generator, and Terminal views.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """


def build_help_menu(window) -> None:
    """
    Builds the Help menu.

    This menu will contain help actions such as opening the user guide, viewing
    keyboard shortcuts, and showing information about SentinelIR.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """