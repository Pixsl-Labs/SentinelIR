# Activating virtual environment
# source venv/bin/activate

# Instantly pull all installed modules into requirements.txt
# pip freeze > requirements.txt

# Standard running command for personal testing
# python3 -m app.main brute_force.log


import argparse
import os
import logging
from colorama import init, Fore

from app.utils.display import (
    print_section_header,
    print_empty_message
)


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            "logs/application.log"
        )
    ]
)

init(autoreset=True)

from app.interaction.interaction import Interaction
from app.runtime.runtime_controller import RunTimeController

from app.log_analyser.log_analyser import LogAnalyser
from app.log_analyser.log_reporter import LogReporter


def run_cli(args):
    analyser = LogAnalyser()
    
    reporter = LogReporter(
        analyser
    )

    log_file = os.path.join(
        "log_files",
        args.file
    )

    controller = RunTimeController(
        analyser,
        reporter,
        log_file
    )

    controller.start()

def run_interactive():
    print_section_header(
        "Interaction Mode"
    )

    analyser = LogAnalyser()

    while True:
        file_name = input("Enter log file name (e.g. auth.log): ").strip()

        if file_name.lower() == "exit":
            print("Exiting...")
            return

        if not file_name:
            print("No file provided. Try again.\n")
            continue

        if not file_name.endswith(".log"):
            file_name += ".log"

        log_file = os.path.join("log_files", file_name)

        if not os.path.exists(log_file):
            print("File not found. Try again.\n")
            continue

        success = analyser.analyse(log_file)

        if not success:
            print_empty_message(
                "Analysis failed. Try again\n"
            )
            
            continue
        
        break
    
    reporter = LogReporter(analyser)

    reporter.print_analysis_summary()

    interaction = Interaction(analyser, reporter)

    interaction.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Analysis Tool")
    parser.add_argument("file", nargs="?", help="Path to log file")
    parser.add_argument("--report", action="store_true", help="Show full report")
    parser.add_argument("--txt", help="Export report to .txt file")
    parser.add_argument("--json", help="Export report to JSON file")

    args = parser.parse_args()

    try:
        if args.file:
            run_cli(args)
        else:
            run_interactive()

    except KeyboardInterrupt:
        print("\n\nExiting...")