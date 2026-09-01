from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD
)

from app.utils.colours import get_attempt_colour
from app.utils.display import (
    print_section_header,
    print_generated_timestamp,
    print_stat_row
)

from app.detection.detection_engine import DetectionEngine

from colorama import Fore


class Summary:
    def print_attack_summary(self) -> None:
        """
        Prints a high-level summary of detected threats.

        Displays the total failed attempts, top attacking IP, most targeted user,
        brute-force alert count, and user-targeting alert count for the analysed data.

        Returns:
            None
        """

        print_section_header(
            "Attack Summary",
            Fore.GREEN
        )

        print_generated_timestamp()

        total_failed = self.get_total_failed_login_attempts()

        top_attacker = None
        top_attacker_colour = Fore.LIGHTBLACK_EX

        if self.analyser.failed_logins:
            top_ip, attempts = max(
                self.analyser.failed_ip_counts.items(),
                key=lambda item: item[1]
            )

            top_attacker = f"{top_ip} ({attempts} attempts)"
            top_attacker_colour = get_attempt_colour(attempts)

        targeted = DetectionEngine.get_user_targeting(
            self.analyser,
            BRUTE_FORCE_THRESHOLD
        )

        most_targeted_user = None
        most_targeted_colour = Fore.LIGHTBLACK_EX

        if targeted:
            top_target = targeted[0]

            most_targeted_user = (
                f"{top_target.username} "
                f"({top_target.attempts} attempts "
                f"from {top_target.unique_ips} IPs)"
            )

            most_targeted_colour = get_attempt_colour(
                top_target.attempts
            )

        brute_force_results = DetectionEngine.get_brute_force(
            self.analyser
        )

        rows = [
            (
                "Total failed attempts",
                total_failed if total_failed else None,
                get_attempt_colour(total_failed)
            ),
            (
                "Top attacking IP",
                top_attacker,
                top_attacker_colour
            ),
            (
                "Most targeted user",
                most_targeted_user,
                most_targeted_colour
            ),
            (
                "Brute-force alerts",
                len(brute_force_results) if brute_force_results else None,
                get_attempt_colour(len(brute_force_results))
            ),
            (
                "User-targeting alerts",
                len(targeted) if targeted else None,
                get_attempt_colour(len(targeted))
            )
        ]

        for label, value, colour in rows:
            print_stat_row(
                label,
                value,
                colour
            )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )
