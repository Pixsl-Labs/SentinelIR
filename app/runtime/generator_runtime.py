from colorama import Fore


from app.utils.display import (
    print_section_header,
    print_empty_message
)
from app.utils.path_validation import validate_input_log_path


from app.runtime.generator_selection import (
    select_scenario_type,
    select_ssh_scenario,
    select_ftp_scenario,
    select_http_scenario,
    select_mixed_services
)


from app.generator.log_generator import (
    write_lines_to_file,
    stream_lines_to_file
)


class GeneratorRuntime:
    """
    Handles the scenario generation runtime workflow.

    This runtime allows the user to select a log scenario, preview the generated
    lines, confirm generation, choose an output file, and write or stream the logs
    into the selected file.
    """

    def start(self) -> None:
        """
        Runs the scenario generator workflow.

        Coordinates scenario selection, preview, confirmation, output file selection,
        write mode selection, and final write or stream behaviour.

        Returns:
            None
        """

        scenario_type = select_scenario_type()

        if scenario_type is None:
            return

        if scenario_type == "SSH":

            selected_scenario = select_ssh_scenario()

        elif scenario_type == "FTP":

            selected_scenario = select_ftp_scenario()

        elif scenario_type == "HTTP":

            selected_scenario = select_http_scenario()

        elif scenario_type == "MIXED":

            selected_scenario = select_mixed_services()

        else:

            print_empty_message(
                "Invalid scenario type choice."
            )

            return

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

    def preview_scenario(
            self,
            scenario_name: str,
            lines: list[str]
            ) -> None:
        """
        Prints a preview of the selected generated scenario.

        Displays the scenario name, number of generated lines, first generated line,
        and last generated line before the user confirms whether to continue.

        Args:
            scenario_name (str): Name of the selected scenario.
            lines (list[str]): Generated log lines to preview.

        Returns:
            None
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
        Asks the user to confirm scenario generation.

        Pressing Enter defaults to yes.

        Returns:
            bool: True if the user confirms, otherwise False.
        """

        while True:
            confirm = input(
                "\nContinue with this scenario? (Y/n): "
            ).strip().lower()

            if confirm in ["", "y", "yes"]:

                return True

            if confirm in ["n", "no"]:

                return False

            print_empty_message(
                "Invalid choice. Press Enter/y for yes or n for no."
            )

    def prepare_output_file(
            self,
            output_file: str,
            append: bool
            ) -> None:
        """
        Prepares the output file before streaming generated logs.

        If append mode is disabled, the output file is cleared before streamed log
        lines are written to it.

        Args:
            output_file (str): Path to the output log file.
            append (bool): Whether generated lines should be appended to the file.

        Returns:
            None
        """

        if not append:
            with open(output_file, "w"):
                pass

    def select_output_file(
            self
            ) -> str | None:
        """
        Prompts the user for the output log file path.

        Uses generated.log as the default file name if no input is provided and ensures
        the selected file name ends with the .log extension.

        Returns:
            str | None: Output log file path.
        """

        file_name = input(
            "\nEnter output log file name (default: generated.log): "
        ).strip()

        if not file_name:
            file_name = "generated.log"

        if not file_name.endswith(".log"):
            file_name += ".log"

        return validate_input_log_path(file_name)

    def select_stream_or_write(
            self,
            output_file: str,
            lines: list[str],
            append: bool
            ) -> None:
        """
        Prompts the user to write or stream generated log lines.

        Allows generated lines to be written instantly, streamed slowly into the output
        file, or cancelled before writing.

        Args:
            output_file (str): Path to the output log file.
            lines (list[str]): Generated log lines to write or stream.
            append (bool): Whether generated lines should be appended to the file.

        Returns:
            None
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
                    + f"{'Mode:'} {self.get_write_mode_label(append)}"
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
        Prompts the user to choose append or overwrite mode.

        Returns:
            bool: True if appending to the existing file, otherwise False.
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
        Converts a write mode boolean into a readable label.

        Args:
            append (bool): Whether append mode is enabled.

        Returns:
            str: Write mode label, either append or overwrite.
        """

        if append is True:

            return "append"

        elif append is False:

            return "overwrite"

        else:

            print_empty_message(
                "Error in write mode selection."
            )

    def select_stream_delay(self) -> float:
        """
        Prompts the user for the stream delay between generated log lines.

        If the user provides no value, an invalid value, or a negative value, the
        default delay is used instead.

        Returns:
            float: Delay in seconds between streamed log lines.
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
