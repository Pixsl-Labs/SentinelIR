"""
Settings menu bar and actions for the SentinelIR GUI.
"""

# from app.gui.menus.menu_helpers import create_action


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
