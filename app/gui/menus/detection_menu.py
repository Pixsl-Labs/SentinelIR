"""
Detection menu bar and actions for the SentinelIR GUI.
"""

from app.gui.menus.menu_helpers import create_action


def build_detection_menu(window) -> None:
    """
    Builds the Detection menu.

    This menu will contain detection-focused actions such as brute-force detection,
    suspicious-success detection, user-targeting detection, suspicious IP review,
    and alert summaries.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """

    detection_menu = window.menuBar().addMenu(
        "&Detection"
    )

    brute_force_detection_action = create_action(
        window=window,
        text="Brute-force Detection",
        icon_name="log_file.png",
        callback=brute_force_detection,
        shortcut="Ctrl+2"
    )

    detection_menu.addAction(
        brute_force_detection_action
    )

    detection_menu.addSeparator()

    suspicious_success_action = create_action(
        window=window,
        text="Suspicious Success",
        icon_name="log_file.png",
        callback=suspicious_success
        # shortcut="Ctrl+..."
    )

    detection_menu.addAction(
        suspicious_success_action
    )

    detection_menu.addSeparator()

    user_targeting_action = create_action(
        window=window,
        text="User Targeting",
        icon_name="log_file.png",
        callback=user_targeting
        # shortcut="Ctrl+..."
    )

    detection_menu.addAction(
        user_targeting_action
    )

    detection_menu.addSeparator()

    suspicious_ips_action = create_action(
        window=window,
        text="Suspicious IPs",
        icon_name="log_file.png",
        callback=suspicious_ips
        # shortcut="Ctrl+..."
    )

    detection_menu.addAction(
        suspicious_ips_action
    )

    detection_menu.addSeparator()

    alert_summary_action = create_action(
        window=window,
        text="Alert Summary",
        icon_name="log_file.png",
        callback=alert_summary
        # shortcut="Ctrl+..."
    )

    detection_menu.addAction(
        alert_summary_action
    )

def brute_force_detection(window) -> None:
    """
    Handles the Brute-force Detection menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Brute-force Detection clicked")

def suspicious_success(window) -> None:
    """
    Handles the Suspicious Success menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Suspicious Success clicked")

def user_targeting(window) -> None:
    """
    Handles the User Targeting menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("User Targeting clicked")

def suspicious_ips(window) -> None:
    """
    Handles the Suspicious IPs menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Suspicious IPs clicked")

def alert_summary(window) -> None:
    """
    Handles the Alert Summary menu action.

    Args:
        window: MainWindow instance.

    Returns:
        None
    """

    print("Alert Summary clicked")