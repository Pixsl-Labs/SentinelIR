from app.config.security_config import (
    BRUTE_FORCE_THRESHOLD,
    BRUTE_FORCE_TIME_WINDOW,
    USER_TARGETING_THRESHOLD
)
from app.detection.alert_types import (
    BRUTE_FORCE_ALERT,
    SUSPICIOUS_SUCCESS_ALERT,
    USER_TARGETING_ALERT
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


class DetectionEngine:

    def __init__(self):
        self.alert_state = {
            BRUTE_FORCE_ALERT: set(),
            SUSPICIOUS_SUCCESS_ALERT: set(),
            USER_TARGETING_ALERT: set()
        }

    def has_alerted(
            self,
            alert_type: str,
            entity: str
    ) -> bool:
        """
        Checks whether an alert has already been raised
        for a specific alert type and entity.
        """

        return entity in self.alert_state.get(alert_type, set())
    
    def mark_alerted(
            self,
            alert_type: str,
            entity: str
    ) -> None:
        """
        Records that an alert has been raised
        for a specific alert type and entity.
        """

        if alert_type not in self.alert_state:
            self.alert_state[alert_type] = set()
        
        self.alert_state[alert_type].add(entity)

    def reset_alert_state(self) -> None:
        """
        Clears all live alert states.
        """

        for alert_entries in self.alert_state.values():
            alert_entries.clear()

    
    def get_alert_count(
            self,
            alert_type: str
    ) -> int:
        """
        Returns the number of alerts raised for a specific alert type.
        """

        return len(
            self.alert_state.get(
                alert_type,
                set()
            )
        )
    
    def get_total_alerts(
            self
    ) -> int:
        """
        Returns the total number of live alerts raised.
        """

        return sum(
            len(alerted_entities)
            for alerted_entities in self.alert_state.values()
        )
    
    def get_alert_summary(
            self
    ) -> dict[str, int]:
        """
        Returns alert counts grouped by alert type.
        """

        return {
            alert_type: len(alerted_entities)
            for alert_type, alerted_entities in self.alert_state.items()
        }
    

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

        self.detect_live_user_targeting(analyser)
        
    def detect_live_brute_force(
            self,
            analyser
        ) -> None:
        """
        Detects live brute-force activity.
        """

        threshold = BRUTE_FORCE_THRESHOLD

        for ip, attempts in analyser.failed_ip_counts.items():

            if (
                attempts >= threshold 
                and not self.has_alerted(BRUTE_FORCE_ALERT, ip)
            ):

                print_alert(
                    severity="HIGH",
                    title="Brute Force Detected",
                    message=(
                        f"IP: {ip} | "
                        f"Attempts: {attempts}\n"
                    )
                )

                self.mark_alerted(
                    BRUTE_FORCE_ALERT,
                    ip
                )

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
                and not self.has_alerted(SUSPICIOUS_SUCCESS_ALERT, entry.ip)
            ):
                
                print_alert(
                    severity="MEDIUM",
                    title="Suspicious Success Detected",
                    message=(
                        f"IP: {entry.ip} | "
                        f"User: {entry.user} | "
                        f"Successful login after failure\n"
                    )
                )

                self.mark_alerted(
                    SUSPICIOUS_SUCCESS_ALERT,
                    entry.ip
                )

    def detect_live_user_targeting(
            self,
            analyser
    ) -> None:
        """
        Detects live user targeting activity.
        """

        user_to_ips = defaultdict(set)

        for entry in analyser.failed_logins:

            user_to_ips[entry.user].add(entry.ip)

        for user, ips in user_to_ips.items():

            unique_ip_count = len(ips)

            if (
                unique_ip_count >= USER_TARGETING_THRESHOLD
                and not self.has_alerted(USER_TARGETING_ALERT, user)
            ):
                
                print_alert(
                    severity="HIGH",
                    title="User Targeting Detected",
                    message=(
                        f"User: {user} | "
                        f"Unique IPs: {unique_ip_count} | "
                        f"Threshold: {USER_TARGETING_THRESHOLD}\n"
                    )
                )

                self.mark_alerted(
                    USER_TARGETING_ALERT,
                    user
                )