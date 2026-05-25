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

    def start(
        self
    ) -> None:
        """
        Runs the scenario generator workflow.
        """

        lines = self.select_scenario()

        if lines is None:

            return
        
        output_file = self.select_output_file()

        if output_file is None:

            return
        
        self.select_stream_or_write(
            output_file,
            lines
        )

    def select_scenario(
            self
    ) -> list[str]:
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

                return generate_brute_force_scenario()
            
            elif choice == "2":

                return generate_suspicious_success_scenario()
            
            elif choice == "3":

                return generate_user_targeting_scenario()
            
            elif choice == "4":

                return generate_normal_activity()
            
            elif choice == "5":

                return generate_mixed_attack_scenario()
            
            elif choice == "6":

                return None
            
            else:

                print_empty_message(
                    "Invalid scenario choice."
                )

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
            lines: list[str]
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
                    append=True
                )

                print(
                    Fore.GREEN
                    + f"\nGenerated {len(lines)} into {output_file}"
                )

                return
            
            if choice == "2":

                stream_lines_to_file(
                    output_file,
                    lines,
                    delay_seconds=0.5
                )

                print(
                    Fore.GREEN
                    + f"\nStreamed {len(lines)} into {output_file}"
                )

                return
            
            if choice == "3":
                
                return
            
            else:

                print_empty_message(
                    "Invalid output mode."
                )