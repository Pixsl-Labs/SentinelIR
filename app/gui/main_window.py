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

from app.gui.styles.light_theme import LIGHT_THEME


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

        self.assets_path = Path(__file__).resolve().parent / "assets"

        label = QLabel("Hello World - SentinelIR GUI")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        self.setStatusBar(QStatusBar(self))

        # --- Menu Bar ---

        menu = self.menuBar()

        # --- File Menu ---

        file_menu = menu.addMenu("&File")

        # --- Open Log File ---

        open_log_action = QAction(
            QIcon(self.get_icon("log_file.png")),
            "Open Log File",
            self
        )

        open_log_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            open_log_action
        )

        file_menu.addSeparator()

        # --- Open Config File ---

        open_config_action = QAction(
            QIcon(self.get_icon("config_file.png")),
            "Open Config File",
            self
        )

        open_config_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            open_config_action
        )

        file_menu.addSeparator()

        # --- Save Config ---

        save_config_action = QAction(
            QIcon(self.get_icon("save_config.png")),
            "Save Config",
            self
        )

        save_config_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            save_config_action
        )

        file_menu.addSeparator()

        # --- Export Report ---

        export_report_action = QAction(
            QIcon(self.get_icon("export_report.png")),
            "Export Report",
            self
        )

        export_report_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            export_report_action
        )

        file_menu.addSeparator()

        # --- Exit ---

        exit_action = QAction(
            QIcon(self.get_icon("exit.png")),
            "Exit",
            self
        )

        exit_action.triggered.connect(
            self.menu_action_clicked
        )

        file_menu.addAction(
            exit_action
        )

        file_menu.addSeparator()

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