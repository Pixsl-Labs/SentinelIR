LIGHT_THEME = """
    QWidget {
        background-color: white;
        color: black;
    }

    QMenuBar {
        background-color: white;
        color: black;
    }

    QMenuBar::item {
        background-color: transparent;
    }

    QMenuBar::item:selected {
        background-color: #f0f0f0;
        color: black;
    }

    QMenuBar::item:pressed {
        background-color: #e5e5e5;
    }

    QMenu {
        background-color: white;
        color: black;
        border: 1px solid #d0d0d0;
    }

    QMenu::item {
        background-color: transparent;
    }

    QMenu::item:selected {
        background-color: #f0f0f0;
        color: black;
    }

    QMenu::separator {
        height: 1px;
        background: #d0d0d0;
    }

    QStatusBar {
        background-color: white;
        color: black;
        border-top: 1px solid #d0d0d0;
    }
"""
