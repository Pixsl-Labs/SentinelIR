from app.interaction.interaction import Interaction

from app.utils.display import (
    print_empty_message
)


class StaticRuntime:
    """
    Handles static log analysis runtime mode.

    This runtime analyses the selected log file once and then starts the
    interactive CLI investigation workflow.
    """

    def __init__(
            self,
            analyser,
            reporter,
            log_file
            ) -> None:
        """
        Initialises the static runtime.

        Args:
            analyser: Log analyser instance used to analyse the selected file.
            reporter: Log reporter instance used by the interaction layer.
            log_file: Path to the log file being analysed.

        Returns:
            None
        """
        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(self) -> None:
        """
        Starts static analysis mode.

        Analyses the configured log file and opens the interaction menu if analysis
        succeeds. If analysis fails, an error message is displayed and the workflow
        stops.

        Returns:
            None
        """

        success = self.analyser.analyse(
            self.log_file
        )

        if not success:

            print_empty_message(
                "Analysis failed."
            )

            return

        interaction = Interaction(
            self.analyser,
            self.reporter
        )

        interaction.run()
