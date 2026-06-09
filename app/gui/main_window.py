"""
Main GUI window for SentinelIR.
"""

# python3 -m app.gui.gui_main

import sys
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

        # --- Shortcuts ---

        # --- Open Log File Shortcut ---

        self.open_file_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_file_shortcut.activated.connect(lambda: self.load_log_file("auth.log"))

        # --- Save Shortcut ---

        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(lambda: self.save("auth.log"))

        # --- Export Report Shortcut ---

        self.export_report_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.export_report_shortcut.activated.connect(lambda: self.save("auth.log"))

        # --- Exit Shortcut ---

        self.exit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.exit_shortcut.activated.connect(lambda: self.exit_application())

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
            self.exit_application
        )

        file_menu.addAction(
            exit_action
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

    def load_log_file(
            self,
            file_path:str
    ) -> None:
        """
        Loads log file for analysis.

        Args:
            file_path (str): File path of file to open.

        Returns:
            None
        """

        print(f"Loading: {file_path}")

    def save(
                self,
                file_path: str
        ) -> None:
        """
        Saves current config file.

        Args:
            file_path (str): File path to save.

        Returns:
            None
        """

        print(f"Saved: {file_path}")

    def export_report(
            self,
            file_path: str,
            output_path: str
    ) -> None:
        """
        Exports a report of the choosen / current log file.

        Args:
            file_path (str): File path to export to a report.
            output_path (str): Output path for the exported report.

        Returns:
            None
        """

        print(f"Exporting report: {file_path} as {output_path}")

    def exit_application(self) -> None:
        """
        Exits SentinelIR GUI.

        Returns:
            None
        """

        self.close()