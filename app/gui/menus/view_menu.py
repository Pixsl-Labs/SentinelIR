"""
View menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


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