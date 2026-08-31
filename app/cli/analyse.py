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
        
    )