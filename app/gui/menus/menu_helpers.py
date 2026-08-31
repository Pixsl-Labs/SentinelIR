"""
Shared menu helper functions for the SentinelIR GUI.
"""

from PySide6.QtGui import QAction

from app.gui.utils.icons import get_icon


def create_action(
        window,
        text: str,
        icon_name: str | None,
        callback,
        shortcut: str | None = None
) -> QAction:
    """
    Creates a reusable menu action.

    Args:
        window: MainWindow instance that owns the action.
        text (str): Text displayed for the menu action.
        icon_name (str | None): Icon filename from app/gui/assets, or None.
        callback: Function called when the action is triggered.
        shortcut (str | None): Optional keyboard shortcut.
            Defaults to None.

    Returns:
        QAction: Configured menu action.
    """

    action = QAction(
        text,
        window
    )

    if icon_name is not None:

        action.setIcon(
            get_icon(icon_name)
        )

    if shortcut is not None:

        action.setShortcut(
            shortcut
        )

    action.triggered.connect(
        lambda checked=False: callback(window)
    )

    return action
