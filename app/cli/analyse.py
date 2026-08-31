"""
Static analysis CLI entry point.
"""

import argparse

from app.cli.common import (
    create_analysis_components,
    prompts_for_log_file,
    resolve_log_file
)

from app.runtime.static_runtime import StaticRuntime

def main() -> None:
    """
    Starts SentinelIR static analysis.
    """

    parser = argparse.ArgumentParser(
        prog="analyse",
        description="Analyse authentication logs with SentinelIR."
    )

    parser.add_argument(
        "file",
        nargs="?",
        metavar="LOG_FILE",
        help="Log file to analyse."
    )

    args = parser.parse_args()

    if args.file:

        try:

            log_file = resolve_log_file(
                args.file
            )

        except FileNotFoundError as e:

            print(e)

            return

    else:

        log_file = prompts_for_log_file()

    analyser, reporter = create_analysis_components()

    runtime = StaticRuntime(
        analyser=analyser,
        reporter=resolve_log_file,
        log_file=str(log_file)
    )

    runtime.start()

if __name__ == "__main__":
    main()