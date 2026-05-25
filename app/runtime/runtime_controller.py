from app.runtime.static_runtime import StaticRuntime
from app.runtime.live_runtime import LiveRuntime
from app.runtime.generator_runtime import GeneratorRuntime

from app.utils.display import (
    print_section_header,
    print_empty_message
)

from colorama import Fore


class RunTimeController:

    def __init__(
            self,
            analyser,
            reporter,
            log_file
        ):
        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(
        self
    ):
        
        while True:

            print_section_header(
                "Runtime Mode",
                Fore.GREEN                
            )
            print("1. Static Analysis")
            print("2. Live Monitoring")
            print("3. Generate Scenario")
            print("4. Exit")

            choice = input("\nSelect mode: (1-4) ").strip()

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

                generatetime = GeneratorRuntime()

                generatetime.start()

            elif choice == "4":

                print("\nExiting application...")
                break

            else:
                
                print_empty_message(
                    "Invalid choice."
                )