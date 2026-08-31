"""
Live Monitoring menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action

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
