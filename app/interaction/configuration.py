from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD,
    BRUTE_FORCE_TIME_WINDOW
)

from app.utils.display import (
    logging_info,
    print_empty_message
)


from app.interaction.menus import display_configuration_menu
from app.interaction.filters import integer_validation


def configure(self) -> None:
    """
    Allows the user to configure detection settings.

    Displays the configuration menu and lets the user update the brute-force
    threshold, update the time window, restore default values, or return to the
    previous menu.

    Args:
        self: Interaction instance containing the current threshold and time
            window settings.

    Returns:
        None
    """

    while True:

        display_configuration_menu(self.threshold, self.window_seconds)

        print(
            f"\nCurrent config: "
            f"threshold={self.threshold}, "
            f"window={self.window_seconds}"
        )

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":

            new_value = integer_validation(
                f"\nEnter max attempts (current = {self.threshold}): ",
                self.threshold,
                label="threshold"
            )

            if new_value != self.threshold:
                self.threshold = new_value

                logging_info(
                    "\nSettings Updated."
                )

        elif choice == "2":

            new_value = integer_validation(
                f"\nEnter time window (current = {self.window_seconds}): ",
                self.window_seconds,
                label="time window"
            )

            if new_value != self.window_seconds:
                self.window_seconds = new_value

                logging_info(
                    "\nSettings Updated."
                )

        elif choice == "3":
            self.threshold = BRUTE_FORCE_THRESHOLD

            self.window_seconds = BRUTE_FORCE_TIME_WINDOW

            print(
                f"\nConfigured settings have now been set back to default "
                f"(threshold={self.threshold}, "
                f"time window={self.window_seconds})"
            )

        elif choice == "4":

            break

        else:

            print_empty_message(
                "Invalid choice. Please try again."
            )
