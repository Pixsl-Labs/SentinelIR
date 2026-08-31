"""
Reports menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


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
