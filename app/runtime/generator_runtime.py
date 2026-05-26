from app.utils.display import (
    print_section_header,
    print_empty_message
)

from app.generator.scenarios import (
    generate_brute_force_scenario,
    generate_mixed_attack_scenario,
    generate_normal_activity,
    generate_suspicious_success_scenario,
    generate_user_targeting_scenario
)
from app.generator.log_generator import (
    write_lines_to_file,
    stream_lines_to_file
)


from colorama import Fore
import os


class GeneratorRuntime:

    def start(self) -> None:
        """
        Runs the scenario generator workflow.
        """

        selected_scenario = self.select_scenario()

        if selected_scenario is None:
            return

        scenario_name, lines = selected_scenario

        self.preview_scenario(
            scenario_name,
            lines
        )

        if not self.confirm_scenario():
            print_empty_message(
                "Scenario generation cancelled."
            )

            return

        output_file = self.select_output_file()

        if output_file is None:
            return
        
        append = self.select_append_mode()

        self.select_stream_or_write(
            output_file,
            lines,
            append
        )

    def select_scenario(
            self
        ) -> tuple[str, list[str]] | None:
        """
        Allows the user to select which log scenario to generate.
        """

        while True:

            print_section_header(
                "Select Scenario:",
                Fore.GREEN
            )

            print("1. Brute force")
            print("2. Suspicious success")
            print("3. User targeting")
            print("4. Normal activity")
            print("5. Mixed attack")
            print("6. Exit")

            choice = input("\nSelect scenario: (1-6) ").strip()

            if choice == "1":

                return "Brute force", generate_brute_force_scenario()
            
            elif choice == "2":

                return "Suspicious success", generate_suspicious_success_scenario()
            
            elif choice == "3":

                return "User targeting", generate_user_targeting_scenario()
            
            elif choice == "4":

                return "Normal activity", generate_normal_activity()
            
            elif choice == "5":

                return "Mixed attack", generate_mixed_attack_scenario()
            
            elif choice == "6":

                return None
            
            else:

                print_empty_message(
                    "Invalid scenario choice."
                )

    def preview_scenario(
            self,
            scenario_name: str,
            lines: list[str]
    ) -> None:
        """
        Prints a short preview of the generated scenario.
        """

        print()
        print_section_header(
            "Scenario Preview",
            Fore.LIGHTGREEN_EX
        )

        print(f"{'Scenario selected:':<18} {scenario_name}\n")

        print(f"{'Generated lines:':<18} {len(lines)}\n")

        if not lines:
            print_empty_message(
                "No lines generated."
            )

        print(f"{'First line:':<18} {lines[0]}\n")
        print(f"{'Last line:':<18} {lines[-1]}")

        print_section_header(
            "End of Scenario Preview",
            Fore.LIGHTGREEN_EX
        )

    def confirm_scenario(self) -> bool:
        """
        Asks the user to confirm whether to continue with the selected scenario.
        """

        confirm = input(
            "\nContinue with this scenario? (y/n): "
        ).strip().lower()

        return confirm == "y"
    
    def prepare_output_file(
            self,
            output_file: str,
            append: bool
        ) -> None:
        """
        Prepares the output file before streaming.
        
        If append is False, the file is cleared before new log lines
        are streamed to it.
        """

        if not append:
            with open(output_file, "w"):
                pass

    def select_output_file(
            self
    ) -> str | None:
        """
        Gets the output log file path from the user.
        """

        file_name = input(
            "\nEnter output log file name (default: generated.log): "
        ).strip()

        if not file_name:
            file_name = "generated.log"

        if not file_name.endswith(".log"):
            file_name += ".log"

        return os.path.join(
            "log_files",
            file_name
        )

    def select_stream_or_write(
            self,
            output_file: str,
            lines: list[str],
            append: bool
        )-> None:
        """
        Allows the user to write or stream generated log lines.
        """

        while True:

            print_section_header(
                "Generator Output Mode",
                Fore.GREEN
            )

            print("1. Write instantly")
            print("2. Stream slowly")
            print("3. Cancel")

            choice = input("\nSelect output mode (1-3): ").strip()

            if choice == "1":

                write_lines_to_file(
                    output_file,
                    lines,
                    append=append
                )

                print_section_header(
                    "Scenario Generation Summary",
                    Fore.LIGHTGREEN_EX
                )

                print(
                    Fore.LIGHTCYAN_EX
                    + f"Generated {len(lines)} lines into {output_file}"
                )

                print(
                    Fore.LIGHTCYAN_EX
                    + f"{'Mode:'} {self.get_write_mode_label(append)}"
                )

                print_section_header(
                    "End of Scenario Generation Summary",
                    Fore.LIGHTGREEN_EX
                )

                return
            
            if choice == "2":

                self.prepare_output_file(
                    output_file,
                    append
                )

                delay_seconds = self.select_stream_delay()

                stream_lines_to_file(
                    output_file,
                    lines,
                    delay_seconds=delay_seconds
                )

                print()

                print_section_header(
                    "Scenario Generation Summary",
                    Fore.LIGHTGREEN_EX
                )

                print(
                    Fore.LIGHTCYAN_EX
                    + f"Streamed {len(lines)} lines into {output_file}"
                )

                print(
                    Fore.LIGHTCYAN_EX
                    + f"{'Delay:'} {delay_seconds} seconds"
                )

                print(
                    Fore.LIGHTCYAN_EX
                    +f"{'Mode:'} {self.get_write_mode_label(append)}"
                )

                print_section_header(
                    "End of Scenario Generation Summary",
                    Fore.LIGHTGREEN_EX
                )

                return
            
            if choice == "3":
                
                return
            
            else:

                print_empty_message(
                    "Invalid output mode."
                )

    def select_append_mode(self) -> bool:
        """
        Allows the user to choose whether to append to or overwrite
        the output log file.

        Returns:
            bool: True if appending, False if overwriting.
        """

        while True:

            print_section_header(
                "File Write Mode",
                Fore.GREEN
            )

            print("1. Append to existing file")
            print("2. Overwrite existing file")

            choice = input("\nSelect write mode (1-2): ").strip()

            if choice == "1":

                return True
            
            elif choice == "2":

                return False
            
            else:

                print_empty_message(
                    "Invalid write mode."
                )

    def get_write_mode_label(
            self,
            append: bool
    ) -> str:
        """
        Converts the boolean into a readable word.
        """

        if append == True:

            return "append"

        elif append == False:

            return "overwrite"
        
        else:

            print_empty_message(
                "Error in write mdoe selection."
            )

    def select_stream_delay(self) -> float:
        """
        Asks the user how fast logs should stream into the file.
        """

        choice = input("\nEnter stream delay seconds (default: 0.5): ").strip()

        if not choice:
            
            return 0.5
        
        try:

            delay = float(choice)

        except ValueError:

            print_empty_message(
                "Invalid input. Using default: 0.5"
            )

            return 0.5
        
        if delay < 0:

            print_empty_message(
                "Negative input. Using default: 0.5"
            )

            return 0.5

        return delay