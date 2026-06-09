"""
Main GUI window for SentinelIR.
"""

# python3 -m app.gui.gui_main

from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QStatusBar,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon


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

        self.assets_path = Path(__file__).resolve().parent / "assets"

        label = QLabel("Hello World - SentinelIR GUI")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        self.setStatusBar(QStatusBar(self))

        # --- Menu Bar ---

        menu = self.menuBar()

        # --- File Menu ---

        file_menu = menu.addMenu("&File")

        open_action = QAction(
            QIcon(self.get_icon("file_icon.png")),
            "Open",
            self
        )

        open_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            open_action
        )

        file_menu.addSeparator()

        close_action = QAction(
            QIcon(self.get_icon("close_icon.png")),
            "Close",
            self
        )

        close_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            close_action
        )

    def get_icon(
            self,
            icon_name: str
    ) -> QIcon:
        """
        Returns an icon from the GUI assets directory.

        Args:
            icon_name (str): Icon filename inside /app/gui/assets.

        Returns:
            QIcon: Loaded Qt icon.
        """

        return QIcon(
            str(self.assets_path / icon_name)
        )

    def menu_action_clicked(
            self
    ) -> None:
        """
        Handles menu action clicks.

        Returns:
            None
        """

        action = self.sender()

        if action:

            print(
                f"Clicked: {action.text()}"
            )