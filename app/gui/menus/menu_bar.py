"""
Menu bar builder for the SentinelIR GUI.
"""

from app.gui.menus.file_menu import build_file_menu
from app.gui.menus.analysis_menu import build_analysis_menu
from app.gui.menus.detection_menu import build_detection_menu
from app.gui.menus.live_monitoring_menu import build_live_monitoring_menu
from app.gui.menus.generator_menu import build_generator_menu
from app.gui.menus.reports_menu import build_reports_menu
from app.gui.menus.settings_menu import build_settings_menu
from app.gui.menus.view_menu import build_view_menu
from app.gui.menus.help_menu import build_help_menu


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