"""
Analysis menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


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

    static_analysis_action = create_action(
        window=window,
        text="Run Static Analysis",
        icon_name="log_file.png",
        callback=run_static_analysis,
        shortcut="Ctrl+2"
    )

    analysis_menu.addAction(
        static_analysis_action
    )

    analysis_menu.addSeparator()

    view_summary_action = create_action(
        window=window,
        text="View Summary",
        icon_name="log_file.png",
        callback=view_summary
        # shortcut="Ctrl+..."
    )

    analysis_menu.addAction(
        view_summary_action
    )

    analysis_menu.addSeparator()

    view_failed_logins_action = create_action(
        window=window,
        text="View Failed Logins",
        icon_name="log_file.png",
        callback=view_failed_logins
        # shortcut="Ctrl+..."
    )

    analysis_menu.addAction(
        view_failed_logins_action
    )

    view_successful_logins_action = create_action(
        window=window,
        text="View Successful Logins",
        icon_name="log_file.png",
        callback=view_successful_logins
        # shortcut="Ctrl+..."
    )

    analysis_menu.addAction(
        view_successful_logins_action
    )

    analysis_menu.addSeparator()

    view_activity_timeline_action = create_action(
        window=window,
        text="View Activity Timeline",
        icon_name="log_file.png",
        callback=view_activity_timeline
        # shortcut="Ctrl+..."
    )

    analysis_menu.addAction(
        view_activity_timeline_action
    )

def run_static_analysis(window) -> None:
    """
    Handles the Run Static Analysis menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Run Static Analysis clicked")

def view_summary(window) -> None:
    """
    Handles the View Summary menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("View Summary clicked")

def view_failed_logins(window) -> None:
    """
    Handles the View Failed Logins menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("View Failed Logins clicked")

def view_successful_logins(window) -> None:
    """
    Handles the View Successful Logins menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("View Successful Logins clicked")

def view_activity_timeline(window) -> None:
    """
    Handles the View Activity Timeline menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("View Activity Timeline clicked")

def clear_analysis(window) -> None:
    """
    Handles the Clear Analysis menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Clear Analysis clicked")