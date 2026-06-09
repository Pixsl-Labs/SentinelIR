from pathlib import Path

from PySide6.QtGui import (
    QIcon
)


def get_icon(
        icon_name: str
    ) -> QIcon:
    """
    Returns an icon from the GUI assets directory.

    Args:
        icon_name (str): Icon filename inside /app/gui/assets.

    Returns:
        QIcon: Loaded Qt icon.
    """
    
    assets_path = Path(__file__).resolve().parent.parent / "assets"

    return QIcon(
        str(assets_path / icon_name)
    )