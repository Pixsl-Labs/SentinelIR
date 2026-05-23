from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD,
    BRUTE_FORCE_TIME_WINDOW
)

from app.models.detection_results import (
    BruteForceResult,
    UserTargetingResult,
    SuspiciousSuccessResult
)

from app.utils.severity import get_severity_level
from app.utils.display import (
    print_alert
)

from collections import defaultdict
from colorama import Fore


class DetectionEngine:

    def __init__(self):
        self.alerted_ips = set()
        self.alerted_success_ips = set()

    @staticmethod
    def get_brute_force(
        analyser,
        threshold=BRUTE_FORCE_THRESHOLD,
        window_seconds=BRUTE_FORCE_TIME_WINDOW
    ) -> list[BruteForceResult]:

        ip_attempts = analyser.group_attempts_by_ip()

        results = []

        for ip, time_stamps in ip_attempts.items():

            time_stamps.sort()

            for i in range(len(time_stamps) - threshold + 1):

                start = time_stamps[i]
                end = time_stamps[i + threshold - 1]

                diff = (end - start).total_seconds()

                if diff <= window_seconds:

                    severity = get_severity_level(threshold)

                    results.append(
                        BruteForceResult(
                            ip=ip,
                            attempts=threshold,
                            time_window=diff,
                            severity=severity
                        )
                    )

                    break

        return results

    @staticmethod
    def get_user_targeting(
        analyser,
        threshold=BRUTE_FORCE_THRESHOLD
    ) -> list[UserTargetingResult]:

        user_attempts = defaultdict(list)

        for entry in analyser.failed_logins:
            user_attempts[entry.user].append(entry.ip)

        results = []

        for user, ips in user_attempts.items():

            unique_ips = set(ips)

            if len(unique_ips) >= threshold:

                severity = get_severity_level(
                    len(unique_ips)
                )

                results.append(
                    UserTargetingResult(
                        username=user,
                        attempts=len(ips),
                        unique_ips=len(unique_ips),
                        severity=severity
                    )
                )

        return results

    @staticmethod
    def get_suspicious_success(
        analyser
    ) -> list[SuspiciousSuccessResult]:

        failed_ips = set(
            entry.ip
            for entry in analyser.failed_logins
        )

        results = []

        for entry in analyser.successful_logins:

            if entry.ip in failed_ips:

                severity = get_severity_level(5)

                results.append(
                    SuspiciousSuccessResult(
                        ip=entry.ip,
                        attempts=1,
                        severity=severity
                    )
                )

        return results
    
    def process_live_detection(
        self,
        analyser
    ) -> None:
        """
        Runs live detections against current state.
        """

        self.detect_live_brute_force(analyser)

        self.detect_live_suspicious_success(analyser)

    def detect_live_brute_force(
            self,
            analyser
        ) -> None:
        """
        Detects live brute-force activity.
        """

        threshold = BRUTE_FORCE_THRESHOLD

        for ip, attempts in analyser.failed_ip_counts.items():

            if attempts >= threshold and ip not in self.alerted_ips:

                print_alert(
                    severity="HIGH",
                    title="Brute Force Detected",
                    message=(
                        f"IP: {ip} | "
                        f"Attempts: {attempts}"
                    )
                )

                self.alerted_ips.add(ip)

    def detect_live_suspicious_success(
            self,
            analyser
        ) -> None:
        """
        Detects successful logins from IPs that previously failed authentication.
        """

        failed_ips = {
            entry.ip
            for entry in analyser.failed_logins
        }

        for entry in analyser.successful_logins:

            if (
                entry.ip in failed_ips
                and entry.ip not in self.alerted_success_ips
            ):
                
                print_alert(
                    severity="MEDIUM",
                    title="Suspicious Success Detected",
                    message=(
                        f"IP: {entry.ip} | "
                        f"User: {entry.user} | "
                        f"Successful login after failure"
                    )
                )

                self.alerted_success_ips.add(entry.ip)