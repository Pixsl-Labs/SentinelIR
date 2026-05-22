from colorama import Fore


from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count,
    print_separator
)


def display_log_analysis_menu() -> None:
    """
    Prints the display menu for Log Analysis

    Returns:
        None
    """
    
    print_section_header(
        "Log Analysis Menu",
        Fore.GREEN
    )

    print("1. Show full report")
    print("2. Show attack summary")
    print("3. Show attack statistics")

    print_section_header(
        "Investigation"
    )

    print("4. Show activity timeline")
    print("5. Show suspicious activity")
    print("6. Show failed login details")
    print("7. Show failed login summary")

    print_section_header(
        "Detection"
    )

    print("8. Show suspicious IPs")
    print("9. Show brute force detection")
    print("10. Show most targeted users")
    print("11. Show suspicious success")
    print("12. Show user-targeted attacks")

    print_section_header(
        "General Information"
    )

    print("13. Show successful logins")
    print("14. Show total failed logins")
    print("15. Show unique IP count")

    print_section_header(
        "Configuration"
    )

    print("16. Export report to file")
    print("17. Analyse new file")
    print("18. Configure settings")
    print("19. Show current configuration")
    print("20. Exit")

    print_section_header(
        "End of Menu",
        Fore.MAGENTA
    )

def display_configuration_menu(threshold: int, window_seconds: int) -> None:
    """
    Prints the configuration menu for alerations to Log Analysis
    
    Returns:
        None
    """

    print_section_header(
        "Configuration Menu",
        Fore.GREEN
    )

    print(f"1. Maximum number of attempts (current = {threshold})")
    print(f"2. Maximum time window (current = {window_seconds})")
    print("3. Convert back to original")
    print("4. Exit")

    print_section_header(
        "End of Menu",
        Fore.MAGENTA
    )

def current_config(threshold: int, window_seconds: int) -> None:
    """
    Prints the current configurations
    
    Returns:
        None
    """
    
    print_separator(
        37
    )

    print_section_header(
        "Current Configuration",
        Fore.GREEN
    )

    print(f"- Threshold: {threshold}")
    print(f"- Time window: {window_seconds}")

    print_section_header(
        "End of Configuration Settings",
        Fore.MAGENTA
    )
    print(
        Fore.MAGENTA
        + "\n=== End of Configuration Settings ===\n"
    )

    print_separator(
        37
    )

def select_analysis_mode() -> str:
    """
    Allows user to select analysis mode.
    """

    while True:

        print_section_header(
            "Analysis Mode",
            Fore.LIGHTGREEN_EX
        )

        print("1. Static Analysis")
        print("2. Dynamic Monitoring")

        choice = input("\nSelect option (1-2): ").strip()

        if choice == "1":
            return "static"
        
        elif choice == "2":
            return "dynamic"
        
        else:

            print_empty_message(
                "Invalid choice."
            )