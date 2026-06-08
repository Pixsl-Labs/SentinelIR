from json import JSONDecodeError
from pathlib import Path

from app.config.config_loader import load_config
from app.runtime.live_runtime import LiveRuntime

from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_info,
    print_stat_row
)

from colorama import Fore


class ConfigRuntime:
    """
    Handles configuration-driven monitoring mode.

    This runtime loads SentinelIR settings from a JSON configuration file and
    starts monitoring based on the configured watched files and live monitoring
    settings.
    """

    def __init__(
            self,
            analyser,
            reporter,
            config_path: str = "sentinel_config.json"
        ) -> None:
        """
        Initialises the configuration runtime.

        Args:
            analyser: Log analyser instance used during monitoring.
            reporter: Log reporter instance available for reporting workflow.
            config_path (str): Path to the SentinelIR configuration file.
                Defaults to "sentinel_config.json".

        Returns:
            None
        """

        self.analyser = analyser
        self.reporter = reporter
        self.config_path = config_path

    def start(self) -> None:
        """
        Starts configuration-driven monitoring.

        Loads the application configuration, displaying the active configuration
        summary, and starts live monitoring for the first configured watched file.

        Returns:
            None
        """

        print_section_header(
            "Config Monitoring Mode",
            Fore.GREEN
        )

        try:

            config = load_config(
                self.config_path
            )

        except FileNotFoundError:

            print_empty_message(
                f"Config file not found: {self.config_path}"
            )

            return
        
        except JSONDecodeError:

            print_empty_message(
                f"Invalid JSON config file: {self.config_path}"
            )

            return
        
        if not config.watched_files:

            print_empty_message(
                "No watched file configured."
            )

            return
        
        self.print_config_summary(
            config
        )

        self.apply_detection_thresholds(
            config
        )

        self.start_configured_monitoring(
            config
        )

    def start_monitoring_file(
                self,
                file_path: str,
                config
        ) -> None:
        """
        Starts live monitoring for a selected configuration file.

        Resets the analyser state, creates a LiveRuntime using configuration values,
        and starts monitoring the selected file.

        Args:
            file_path (str): Selected watched file path.
            config: Application configuration object loaded from JSON.

        Returns:
            None
        """

        self.analyser.reset()

        runtime = LiveRuntime(
            analyser=self.analyser,
            reporter=self.reporter,
            log_file=file_path,
            show_new_logs=config.live_monitoring.show_new_logs,
            status_interval=config.live_monitoring.status_interval,
            poll_interval=config.live_monitoring.poll_interval,
            mode_title="Config Monitoring Mode"
        )

        runtime.start()

    def start_configured_monitoring(
                self,
                config
        ) -> None:
        """
        Starts monitoring using configured watched files.

        Validates configured watched files, prompts the user to select one, and then
        starts live monitoring for the selected file.

        Args:
            config: Application configuration object loaded from JSON.

        Returns:
            None
        """

        if not self.validate_watched_files(config.watched_files):

            return
        
        selected_file = self.select_watched_files(
            config.watched_files
        )

        if selected_file is None:

            print_empty_message(
                "Config monitoring cancelled."
            )

            return
        
        self.start_monitoring_file(
            selected_file,
            config
        )

    def apply_detection_thresholds(
                self,
                config
        ) -> None:
        """
        Applies configured threshold values to the detection engine.

        Updates the analyser detection engine so live monitoring uses threshold
        values loaded from the JSON configuration file.

        Args:
            config: Application configuration object loaded from JSON.

        Returns:
            None
        """

        self.analyser.detection_engine.configure_threshold(
            brute_force_threshold=config.thresholds.brute_force_threshold,
            brute_force_time_window=config.thresholds.brute_force_time_window,
            user_targeting_threshold=config.thresholds.user_targeting_threshold
        )

    def validate_watched_files(
                self,
                watched_files: list[str]
        ) -> bool:
        """
        Validates that all configured watched files exist.

        Checks each file path listed in the configuration before monitoring starts.
        If any configured file is missing, an error message is printed and monitoring
        does not continue.

        Args:
            watched_files (list[str]): File paths loaded from the configuration.

        Returns:
            bool: True if all watched files exist, otherwise False.
        """

        missing_files = []

        for file_path in watched_files:

            if not Path(file_path).exists():

                missing_files.append(file_path)

        if missing_files:

            print_empty_message(
                "One or more configured watched files do not exist."
            )

            for file_path in missing_files:

                print_empty_message(
                    f"- {file_path}"
                )

            return False
        
        return True
    
    def select_watched_files(
                self,
                watched_files: list[str]
        ) -> str | None:
        """
        Prompts the user to select a configured watched file.

        Displays each configured watched file as a numbered option and returns the
        selected file path. The user can also cancel and return without starting
        monitoring.

        Args:
            watched_files (list[str]): File paths loaded from the configuration.

        Returns:
            str | None: Selected watched file path, or None if the user cancels.
        """

        while True:

            print_section_header(
                "Configured Watched Files",
                Fore.GREEN
            )

            for index, file_path in enumerate(watched_files, start=1):

                print(f"{index}. {file_path}")
            
            exit_option = len(watched_files) + 1

            print(f"{exit_option}. Cancel\n")

            choice = input(
                f"Select watched file: (1-{exit_option}) "
            ).strip()

            if not choice.isdigit():

                print_empty_message(
                    "Invalid choice."
                )

                continue

            choice_number = int(choice)

            if choice_number == exit_option:

                return None
            
            if 1 <= choice_number <= len(watched_files):

                return watched_files[choice_number - 1]
            
            print_empty_message(
                "Invalid watched file choice."
            )

    def print_config_summary(
                self,
                config
        ) -> None:
        """
        Prints a summary of the loaded configuration.

        Args:
            config: Application configuration object loaded from JSON.

        Returns:
            None
        """

        print_section_header(
            "Loaded Configuration",
            Fore.LIGHTGREEN_EX
        )

        print_stat_row(
            "Config file",
            self.config_path,
            Fore.LIGHTCYAN_EX,
            28
        )

        print_stat_row(
            "Watched files",
            len(config.watched_files),
            Fore.LIGHTCYAN_EX,
            28
        )

        print_stat_row(
            "First watched file",
            len(config.watched_files),
            Fore.LIGHTCYAN_EX,
            28
        )

        for index, file_path in enumerate(config.watched_files, start=1):

            print_stat_row(
                f"File {index}",
                file_path,
                Fore.LIGHTCYAN_EX,
                28
            )

        print_stat_row(
            "Brute-force threshold",
            config.thresholds.brute_force_threshold,
            Fore.LIGHTYELLOW_EX,
            28
        )

        print_stat_row(
            "Brute-force time window",
            config.thresholds.brute_force_time_window,
            Fore.LIGHTYELLOW_EX,
            28
        )

        print_stat_row(
            "User-targeting threshold",
            config.thresholds.user_targeting_threshold,
            Fore.LIGHTYELLOW_EX,
            28
        )

        print_stat_row(
            "Poll interval",
            config.live_monitoring.poll_interval,
            Fore.LIGHTYELLOW_EX,
            28
        )

        print_stat_row(
            "Status interval",
            config.live_monitoring.status_interval,
            Fore.LIGHTYELLOW_EX,
            28
        )

        print_stat_row(
            "Show new logs",
            config.live_monitoring.show_new_logs,
            Fore.LIGHTYELLOW_EX,
            28
        )