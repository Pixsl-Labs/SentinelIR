"""
Main GUI window for SentinelIR.
"""

# source venv/bin/activate
# python3 -m app.gui.gui_main

from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QStatusBar
)

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction,
    QIcon,
    QKeySequence,
    QShortcut
)

from app.gui.styles.light_theme import LIGHT_THEME
from app.gui.utils.icons import (
    get_icon
)
from app.gui.menus.menu_bar import build_menu_bar


class MainWindow(QMainWindow):
    """
    Main application window for the SentinelIR GUI.
    """

    def __init__(self) -> None:
        """
        Initialises the main GUI window.

        Returns:
            None
        """

        super().__init__()

        self.setWindowTitle("SentinelIR")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(LIGHT_THEME)

        label = QLabel("Hello World - SentinelIR GUI")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        self.setStatusBar(QStatusBar(self))

        build_menu_bar(
            self
        )