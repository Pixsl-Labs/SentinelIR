from app.runtime.static_runtime import StaticRuntime
from app.runtime.live_runtime import LiveRuntime
from app.runtime.generator_runtime import GeneratorRuntime

from app.runtime.config_runtime import ConfigRuntime

from app.utils.display import (
    print_section_header,
    print_empty_message
)

from colorama import Fore


class RunTimeController:
    """
    Controls the selected application runtime mode.

    The runtime controller displays the top-level runtime menu and routes the user
    to the static analysis, live monitoring, scenario generation, or application exit.
    """

    def __init__(
            self,
            analyser,
            reporter,
            log_file
        ) -> None:
        """
        Initialises the runtime controller.

        Args:
            analyser: Log analyser instance shared between runtime modes.
            reporter: Log reporter instance used by analysis workflows.
            log_file: Path to the selected log file.

        Returns:
            None
        """
        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(
            self
        ) -> None:
        """
        Runs the runtime mode selection loop.

        Displays available runtime mode and starts the selected workflow. The loop
        continues until the user chooses to exit.

        Returns:
            None
        """
        
        while True:

            print_section_header(
                "Runtime Mode",
                Fore.GREEN                
            )
            
            print("1. Static Analysis")
            print("2. Live Monitoring")
            print("3. Generate Scenario")
            print("4. Config Monitoring")
            print("5. Exit")

            choice = input("\nSelect mode: (1-5) ").strip()

            if choice == "1":

                runtime = StaticRuntime(
                    self.analyser,
                    self.reporter,
                    self.log_file
                )

                runtime.start()

            elif choice == "2":

                runtime = LiveRuntime(
                    self.analyser,
                    self.reporter,
                    self.log_file
                )

                runtime.start()

            elif choice == "3":

                runtime = GeneratorRuntime()

                runtime.start()

            elif choice == "4":

                runtime = ConfigRuntime(
                    self.analyser,
                    self.reporter
                )

                runtime.start()

            elif choice == "5":

                print("\nExiting application...\n")
                break

            else:
                
                print_empty_message(
                    "Invalid choice."
                )