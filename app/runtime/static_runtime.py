from app.interaction.interaction import Interaction

from app.utils.display import (
    print_empty_message
)

class StaticRuntime:

    def __init__(
            self,
            analyser,
            reporter,
            log_file
        ):
        self.analyser = analyser
        self.reporter = reporter
        self.log_file = log_file

    def start(self):

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