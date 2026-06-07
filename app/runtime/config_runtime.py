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

        watched_file = config.watched_files[0]

        if not Path(watched_file).exists:

            print_empty_message(
                f"Watched file does not exist: {watched_file}"
            )

            return
        
        self.analyser.reset()

        runtime = LiveRuntime(
            analyser=self.analyser,
            reporter=self.reporter,
            log_file=watched_file,
            show_new_logs=config.live_monitoring.show_new_logs,
            status_interval=config.live_monitoring.status_interval,
            poll_interval=config.live_monitoring.poll_interval,
            mode_title="Config Monitoring Mode"
        )

        runtime.start()

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
            Fore.CYAN,
            28
        )

        print_stat_row(
            "Watched files",
            len(config.watched_files),
            Fore.CYAN,
            28
        )

        print_stat_row(
            "First watched files",
            config.watched_files[0] if config.watched_files else None,
            Fore.CYAN,
            28
        )

        print_stat_row(
            "Poll interval",
            config.live_monitoring.poll_interval,
            Fore.CYAN,
            28
        )

        print_stat_row(
            "Status interval",
            config.live_monitoring.status_interval,
            Fore.CYAN,
            28
        )

        print_stat_row(
            "Show new logs interval",
            config.live_monitoring.show_new_logs,
            Fore.CYAN,
            28
        )

        print_info(
            "\nStarting configured monitoring...\n",
            Fore.GREEN
        )