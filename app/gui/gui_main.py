"""
GUI entry point for SentinelIR.
"""

import sys

from PySide6.QtWidgets import QApplication

from app.gui.main_window import MainWindow


def run_gui() -> None:
    """
    Starts the SentinelIR GUI application.

    Returns:
        None
    """

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()