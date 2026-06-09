"""
Detection menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


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