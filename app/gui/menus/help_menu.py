"""
Help menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


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