import os
from colorama import Fore

from app.log_analyser.log_analyser import LogAnalyser
from app.log_analyser.log_reporter import LogReporter

from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD, 
    BRUTE_FORCE_TIME_WINDOW
)

from app.interaction.menus import (
    display_log_analysis_menu, 
    current_config
)
from app.interaction.filters import (
    integer_validation, 
    handle_filter_menu, 
    collect_filter_values
)
from app.interaction.configuration import configure
from app.utils.colours import (
    get_count_colour, 
    get_attempt_colour
)
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count,
    print_generated_timestamp
)


class Interaction:
    """
    Provides the main command-line interaction layer for SentinelIR.

    The interaction layer displays menus, collects user choice, triggers
    reporting and detection actions, applies filters, handles exports, and allows
    configuration changes during static analysis mode.
    """
    
    def __init__(self, analyser, reporter):
        """
        Initialises the interaction controller.

        Stores the analyser and reporter instances used throughout the CLI workflow,
        sets the running state, and loads the default detection threshold and time
        window settings.

        Args:
            analyser: Log analyser instance containing parsed authentication data.
            reporter: Log reporter instance used to print reports, summaries, and
                investigation results.

        Returns:
            None
        """
        self.analyser: LogAnalyser = analyser
        self.reporter: LogReporter = reporter
        self.running = True
        self.threshold = BRUTE_FORCE_THRESHOLD
        self.window_seconds = BRUTE_FORCE_TIME_WINDOW

    def run(self) -> None:
        """
        Runs the main interaction loop.

        Displays the log analysis menu, processes the selected option, and calls the
        matching report, investigation, detection, export, or configuration workflow.
        The loop continues until the user chooses to exit.

        Returns:
            None
        """

        while self.running:

            display_log_analysis_menu()

            choice = input(
                "\nSelect an option (1-21): "
            ).strip()

            if choice == "1":
                current_config(self.threshold, self.window_seconds)

                print_section_header(
                    "Log Analysis Report",
                    Fore.GREEN
                )

                print_generated_timestamp()

                if not self.analyser.failed_logins and not self.analyser.successful_logins:
                    print_empty_message(
                        "Log file contained no relevant login activity.\n"
                    )

                print_section_header(
                    "Attention Needed",
                    Fore.LIGHTRED_EX
                )

                total_ips = self.reporter.get_total_number_of_unique_ip_addresses()
                
                total_failed = self.reporter.get_total_failed_login_attempts()

                failed_attempt_colour = get_count_colour(total_failed)
            
                print(
                    Fore.CYAN
                    + f"Unique IP Addresses: {total_ips:>7}\n"
                    + f"{failed_attempt_colour}"
                    + f"Failed Login Attempts: {total_failed:>5}"
                )

                self.reporter.print_suspicious_ips()

                self.reporter.print_failed_logins_summary()

                self.reporter.print_brute_force_results(self.threshold, self.window_seconds)

                self.reporter.print_most_targeted_user()

                self.reporter.print_suspicious_success()

                self.reporter.print_user_targeting(self.threshold)

                self.reporter.print_anonymous_ftp_logins()

                print_section_header(
                    "Standard Logins"
                )

                self.reporter.print_successful_logins()

                print_section_header(
                    "End of Report",
                    Fore.MAGENTA
                )

            elif choice == "2":

                self.reporter.print_attack_summary()

            elif choice == "3":

                self.reporter.print_attack_statistics()

            # === Investigation ===

            elif choice == "4":

                handle_filter_menu(
                    reporter=self.reporter,
                    title="Timeline",
                    show_function=self.reporter.print_activity_timeline,
                    filters=[
                        "service",
                        "username",
                        "ip",
                        "severity",
                        "status",
                        "method",
                        "path",
                        "status_code"
                    ]
                )

            elif choice == "5":

                handle_filter_menu(
                    reporter=self.reporter,
                    title="Suspicious Activity",
                    show_function=self.reporter.print_suspicious_activity,
                    filters=[
                        "service",
                        "ip",
                        "username",
                        "severity",
                        "status",
                        "method",
                        "path",
                        "status_code"
                    ]
                )

            elif choice == "6":

                handle_filter_menu(
                    reporter=self.reporter,
                    title="Failed Logins",
                    show_function=self.reporter.print_failed_logins,
                    filters=[
                        "service",
                        "ip",
                        "username",
                        "severity",
                        "status",
                        "method",
                        "path",
                        "status_code"
                    ]
                )

            elif choice == "7":

                self.reporter.print_failed_logins_summary()

            # === Detection ===
            
            elif choice == "8":

                handle_filter_menu(
                    reporter=self.reporter,
                    title="Suspicious IPs",
                    show_function=self.reporter.print_suspicious_ips,
                    filters=[
                        "service",
                        "ip",
                        "severity"
                    ]
                )

            elif choice == "9":

                threshold = integer_validation(
                    f"\nEnter threshold (default = {self.threshold}): ",
                    self.threshold,
                    label="threshold"
                )

                window_seconds = integer_validation(
                    f"Enter time window (default = {self.window_seconds}): ",
                    self.window_seconds,
                    label="time window"
                )

                self.reporter.print_brute_force_results(
                    threshold,
                    window_seconds
                )

            elif choice == "10":

                self.reporter.print_most_targeted_user()

            elif choice == "11":

                self.reporter.print_suspicious_success()

            elif choice == "12":

                threshold = integer_validation(
                    f"\nEnter threshold (default = {self.threshold}): ",
                    self.threshold,
                    label="threshold"
                )

                self.reporter.print_user_targeting(threshold)

            elif choice == "13":

                self.reporter.print_anonymous_ftp_logins()

            # === General Information ===

            elif choice == "14":

                handle_filter_menu(
                    reporter=self.reporter,
                    title="Successful Logins",
                    show_function=self.reporter.print_successful_logins,
                    filters=[
                        "service",
                        "ip",
                        "username",
                        "severity",
                        "status",
                        "method",
                        "path",
                        "status_code"
                    ]
                )

            elif choice == "15":

                total_failed_ = self.reporter.get_total_failed_login_attempts()

                total_colour_failed = get_attempt_colour(total_failed_)

                print_section_header(
                    "Total Failed Login Attempts",
                    Fore.LIGHTGREEN_EX
                )

                print_total_count(
                    "Total failed logins",
                    total_failed_,
                    total_colour_failed
                )

                print(
                    Fore.MAGENTA
                    + "=== End of Report ==="
                )

            elif choice == "16":

                total_ips = self.reporter.get_total_number_of_unique_ip_addresses()

                total_colour_ips = get_attempt_colour(total_ips)

                print_section_header(
                    "Unique IP Count",
                    Fore.LIGHTGREEN_EX
                )

                print_total_count(
                    "Unique IP count",
                    total_ips,
                    total_colour_ips
                )

                print(
                    Fore.MAGENTA
                    + "=== End of Report ==="
                )

            # === Configuration ===

            elif choice == "17":

                print_section_header(
                    "Export Options",
                    Fore.GREEN
                )

                print("1. Failed Logins")
                print("2. Successful Logins")
                print("3. Activity Timeline")

                export_reports = {
                    "1": {
                        "title": "Failed Logins",
                        "getter": self.reporter.get_failed_logins,
                        "filters": [
                            "service",
                            "ip",
                            "username",
                            "severity",
                            "status",
                            "method",
                            "path",
                            "status_code"
                        ]
                    },

                    "2": {
                        "title": "Successful Logins",
                        "getter": self.reporter.get_successful_logins,
                        "filters": [
                            "service",
                            "ip",
                            "username",
                            "severity",
                            "status",
                            "method",
                            "path",
                            "status_code"
                        ]
                    },

                    "3": {
                        "title": "Activity Timeline",
                        "getter": self.reporter.get_activity_timeline,
                        "filters": [
                            "service",
                            "ip",
                            "username",
                            "severity",
                            "status",
                            "method",
                            "path",
                            "status_code"
                        ]
                    }
                }

                export_choice = input(
                    "\nSelect export option: "
                ).strip()

                export_config = export_reports.get(
                    export_choice
                )

                if export_config is None:

                    print_empty_message(
                        "Invalid export option."
                    )

                    continue

                title = export_config["title"]

                getter = export_config["getter"]

                filters = export_config["filters"]

                filter_values = collect_filter_values(
                    reporter=self.reporter,
                    title=title,
                    filters=filters
                )

                if filter_values is None:

                    continue

                data = getter(
                    **filter_values
                )

                file_path = input(
                    "\nEnter report filename (.txt/.json): "
                ).strip()

                file_path = os.path.join(
                    "reports",
                    file_path
                )

                if file_path.endswith(".txt"):

                    self.reporter.export_txt(
                        file_path,
                        title,
                        data,
                        filters=filter_values
                    )

                elif file_path.endswith(".json"):

                    self.reporter.export_json(
                        file_path,
                        title,
                        data,
                        filters=filter_values
                    )

                else:

                    print_empty_message(
                        "Invalid file extension."
                    )

            elif choice == "18":

                file_path = input("Enter log file path: ")

                self.analyser.reset()

                file_path = "log_files/" + file_path

                self.analyser.analyse(file_path)

            elif choice == "19":
                
                configure(self)

            elif choice == "20":

                current_config(self.threshold, self.window_seconds)
            
            elif choice == "21":

                print(
                    Fore.LIGHTGREEN_EX
                    +"Goodbye!"
                )

                self.running = False           

            else:

                print_empty_message(
                    "Invalid choice. Please try again."
                )