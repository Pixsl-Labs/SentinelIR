"""
Generator menu bar and actions for the SentinelIR GUI.
"""

# from app.gui.menus.menu_helpers import create_action


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
