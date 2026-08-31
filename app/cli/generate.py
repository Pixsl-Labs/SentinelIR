"""
Scenario generation CLI entry point.
"""

from app.cli.common import (
    initialise_cli
)

from app.runtime.generator_runtime import GeneratorRuntime


def main() -> None:
    """
    Starts the SentinelIR scenario generator.
    """

    initialise_cli()

    runtime = GeneratorRuntime()

    runtime.start()

if __name__ == "__main__":
    main()