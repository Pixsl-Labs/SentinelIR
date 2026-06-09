"""
Main GUI window for SentinelIR.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout
)

from PySide6.QtCore import Qt


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

        label = QLabel("Hello World - SentinelIR GUI")
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)