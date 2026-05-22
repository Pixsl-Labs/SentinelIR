from datetime import datetime
from colorama import Fore

from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD
)
from app.utils.colours import get_attempt_colour
from app.utils.display import (
    print_section_header,
    print_empty_message,
    print_total_count
)

from app.detection.detection_engine import DetectionEngine


class Summary:
    def print_attack_summary(self) -> None:
        """
        Prints a high-level summary of detected threats.
        """

        print_section_header(
            "Attack Summary",
            Fore.GREEN
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(
            Fore.CYAN
            + f"Generated: {now}\n"
        )

        total_failed = (
            self.get_total_failed_login_attempts()
        )

        failed_colour = get_attempt_colour(
            total_failed
        )

        print(
            f"{'Total failed attempts:':<25} "
            f"{failed_colour}"
            f"{total_failed if total_failed else 'None'}"
        )

        if self.analyser.failed_logins:

            top_ip, attempts = max(
                self.analyser.failed_ip_counts.items(),
                key=lambda x: x[1]
            )

            attacker_colour = get_attempt_colour(
                attempts
            )

            print(
                f"{'Top attacking IP:':<25} "
                f"{attacker_colour}"
                f"{top_ip} ({attempts} attempts)"
            )

        else:

            print(
                f"{'Top attacking IP:':<25} "
                f"{Fore.LIGHTBLACK_EX}"
                f"None"
            )

        targeted = DetectionEngine.get_user_targeting(self.analyser)

        if targeted:

            top_target = targeted[0]

            targeted_colour = get_attempt_colour(
                top_target.attempts
            )

            print(
                f"{'Most targeted user:':<25} "
                f"{targeted_colour}"
                f"{top_target.username} "
                f"({top_target.attempts} attempts "
                f"from {top_target.unique_ips} IPs)"
            )

        else:

            print(
                f"{'Most targeted user:':<25} "
                f"{Fore.LIGHTBLACK_EX}"
                f"None"
            )

        brute = DetectionEngine.get_brute_force(self.analyser)

        brute_colour = get_attempt_colour(
            len(brute)
        )

        print(
            f"{'Brute-force alerts:':<25} "
            f"{brute_colour}"
            f"{len(brute) if brute else 'None'}"
        )

        targeting = DetectionEngine.get_user_targeting(
            self.analyser,
            BRUTE_FORCE_THRESHOLD
        )

        targeting_colour = get_attempt_colour(
            len(targeting)
        )

        print(
            f"{'User-targeting alerts:':<25} "
            f"{targeting_colour}"
            f"{len(targeting) if targeting else 'None'}"
        )

        print_section_header(
            "End of Report",
            Fore.MAGENTA
        )