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
    SuspiciousSuccessResult,
    AnonymousFTPResult
)

from app.utils.severity import get_severity_level
from app.utils.display import (
    print_alert
)

from collections import defaultdict


class DetectionEngine:
    """
    Handles static and live detection logic for authentication log analysis.

    The detection engine identifies suspicious authentication behaviour such as
    brute-force attacks, successful logins after failed attempts, and distributed
    user-targeting activity. It also tracks live alert state so repeated alerts
    for the same entity can be suppressed during real-time monitoring.
    """

    def __init__(
            self,
            brute_force_threshold: int = BRUTE_FORCE_THRESHOLD,
            brute_force_time_window: int = BRUTE_FORCE_TIME_WINDOW,
            user_targeting_threshold: int = USER_TARGETING_THRESHOLD
        ) -> None:
        """
        Initialises the detection engine alert state and threshold settings.

        The alert state stores which entities have already triggered each live alert
        type. Threshold values control when live detections should trigger alerts.

        Args:
            brute_force_threshold (int): Failed login threshold required to trigger
                brute-force detection. Defaults to BRUTE_FORCE_THRESHOLD.
            brute_force_time_window (int): Time window used for brute-force detection.
                Defaults to BRUTE_FORCE_TIME_WINDOW.
            user_targeting_threshold (int): Unique IP threshold required to trigger
                user-targeting detection. Defaults to USER_TARGETING_THRESHOLD.

        Returns:
            None
        """

        self.brute_force_threshold = brute_force_threshold
        self.brute_force_time_window = brute_force_time_window
        self.user_targeting_threshold = user_targeting_threshold

        self.alert_state = {
            BRUTE_FORCE_ALERT: set(),
            SUSPICIOUS_SUCCESS_ALERT: set(),
            USER_TARGETING_ALERT: set()
        }

    def configure_threshold(
            self,
            brute_force_threshold: int | None = None,
            brute_force_time_window: int | None = None,
            user_targeting_threshold: int | None = None
        ) -> None:
        """
        Updates detection threshold settings.

        Any value left as None keeps the current settings. This allows runtime modes
        such as config monitoring to update detection thresholds without recreating
        the detection engine.

        Args:
            brute_force_threshold (int | None): New brute-force failed login threshold.
                Defaults to None.
            brute_force_time_window (int | None): New brute-force time window.
                Defaults to None.
            user_targeting_threshold (int | None): New user-targeting unique IP
                threshold. Defaults to None.

        Returns:
            None
        """

        if brute_force_threshold is not None:
            self.brute_force_threshold = brute_force_threshold

        if brute_force_time_window is not None:
            self.brute_force_time_window = brute_force_time_window

        if user_targeting_threshold is not None:
            self.user_targeting_threshold = user_targeting_threshold

    def has_alerted(
            self,
            alert_type: str,
            entity: str
    ) -> bool:
        """
        Checks whether an alert has already been raised for an entity.

        Args:
            alert_type (str): The type of alert being checked.
            entity (str): The entity being checked, such as an IP address
            or username.

        Returns:
            bool: True if the entity has already triggered the alert type,
            otherwise False.
        """

        return entity in self.alert_state.get(alert_type, set())
    
    def mark_alerted(
            self,
            alert_type: str,
            entity: str
    ) -> None:
        """
        Records that an entity has triggered a specific alert type.

        Args:
            alert_type: The type of alert being recorded.
            entity (str): The entity that triggered the alert, such as an
            IP address or username.

        Returns:
            None
        """

        if alert_type not in self.alert_state:
            self.alert_state[alert_type] = set()
        
        self.alert_state[alert_type].add(entity)

    def reset_alert_state(self) -> None:
        """
        Clears all live alert tracking state.

        This is used when the analyser is reset so that future monitoring
        sessions or analyses do not reuse alert state from previous runs.

        Returns:
            None
        """

        for alert_entries in self.alert_state.values():
            alert_entries.clear()

    
    def get_alert_count(
            self,
            alert_type: str
    ) -> int:
        """
        Returns the number of entities that triggered a specific alert type.

        Args:
            alert_type (str): The alert type to count.

        Returns:
            int: Number of unique entities that have triggered the alert type.
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
        Returns the total number of live alerts raised across all alert types.

        Returns:
            int: Total number of live alerts recorded by the detection engine.
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

        Each alert type is mapped to the number of unique entities that have
        triggered that alert during live monitoring.

        Returns:
            dict[str, int]: Dictionary containing alert types and their counts.
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
        """
        Detects brute-force activity from failed login timestamps.

        Groups failed login attempts by service and IP address, then checks whether
        each service/IP pair reaches the configured threshold within the configured
        time window.

        Args:
            analyser: Log analyser instance containing failed login entries.
            threshold (int): Number of failed attempts required to trigger a
                brute-force result.
            window_seconds (int): Maximum time window, in seconds, allowed between
                the first and final failed attempt.

        Returns:
            list[BruteForceResult]: Brute-force detection results containing the
                service, attacking IP address, attempt count, time window, and severity.
        """

        grouped_attempts = defaultdict(list)

        for entry in analyser.failed_logins:

            key = (
                entry.service,
                entry.ip
            )

            grouped_attempts[key].append(
                entry.timestamp
            )

        results = []

        for (service, ip), timestamp in grouped_attempts.items():

            timestamp.sort()

            for index in range(len(timestamp) - threshold + 1):

                start = timestamp[index]
                end = timestamp[index + threshold - 1]

                diff = (end - start).total_seconds()

                if diff <= window_seconds:

                    severity = get_severity_level(threshold)

                    results.append(
                        BruteForceResult(
                            service=service,
                            ip=ip,
                            attempts=threshold,
                            time_window=diff,
                            severity=severity
                        )
                    )

                    break

        return results

    @staticmethod
    def get_suspicious_success(
        analyser
    ) -> list[SuspiciousSuccessResult]:
        """
        Detects successful logins from service/IP pairs that previously failed
        authentication.

        Args:
            analyser: Log analyser instance containing failed and successful login
            entries.

        Returns:
            list[SuspiciousSuccessResult]: Suspicious success results containing
            the service, IP address, failed attempt count, and severity.
        """

        failed_attempts = defaultdict(int)

        for entry in analyser.failed_logins:

            key = (
                entry.service,
                entry.ip
            )

            failed_attempts[key] += 1

        results = []

        for entry in analyser.successful_logins:

            key = (
                entry.service,
                entry.ip
            )

            if key in failed_attempts:

                severity = get_severity_level(
                    failed_attempts[key]
                )

                results.append(
                    SuspiciousSuccessResult(
                        service=entry.service,
                        ip=entry.ip,
                        attempts=failed_attempts[key],
                        severity=severity
                    )
                )

        return results
    
    @staticmethod
    def get_user_targeting(
        analyser,
        threshold=USER_TARGETING_THRESHOLD
    ) -> list[UserTargetingResult]:
        """
        Detects distributed user-targeting activity.

        Groups failed login attempts by service and username, then checks whether a
        user has been targeted by enough unique IP addresses within that service.

        Args:
            analyser: Log analyser instance containing failed login entries.
            threshold (int): Number of unique IP addresses required to trigger a
                user-targeting result.

        Returns:
            list[UserTargetingResult]: User-targeting results containing the service,
                username, total attempts, unique IP count, and severity.
        """

        user_attempts = defaultdict(list)

        for entry in analyser.failed_logins:

            key = (
                entry.service,
                entry.user
            )

            user_attempts[key].append(
                entry.ip
            )

        results = []

        for (
            service,
            user
        ), ips in user_attempts.items():

            unique_ips = set(
                ips
            )

            if len(unique_ips) >= threshold:

                severity = get_severity_level(
                    len(unique_ips)
                )

                results.append(
                    UserTargetingResult(
                        service=service,
                        username=user,
                        attempts=len(ips),
                        unique_ips=len(unique_ips),
                        severity=severity
                    )
                )

        return results
    
    @staticmethod
    def get_anonymous_ftp_logins(
            analyser
        ) -> list[AnonymousFTPResult]:
        """
        Detects successful anonymous FTP logins.

        Args:
            analyser: Log analyser instance containing successful login entries.

        Returns:
            list[AnonymousFTPResult]: Anonymous FTP login detection results.
        """

        results = []

        for entry in analyser.successful_logins:

            if (
                entry.service == "FTP"
                and entry.user.lower() == "anonymous"
                and entry.status == "SUCCESS"
            ):
                
                results.append(
                    AnonymousFTPResult(
                        ip=entry.ip,
                        username=entry.user,
                        attempts=1,
                        severity="MEDIUM"
                    )
                )
        
        return results
    
    def process_live_detection(
            self,
            analyser
        ) -> None:
        """
        Runs all live detection checks against the current analyser state.

        This method is called during live monitoring after a new relevant log event
        has been processed.

        Args:
            analyser: Log analyser instance containing the current live login state.

        Returns:
            None
        """

        self.detect_live_brute_force(analyser)

        self.detect_live_suspicious_success(analyser)

        self.detect_live_user_targeting(analyser)
        
    def detect_live_brute_force(
            self,
            analyser
        ) -> None:
        """
        Detects live brute-force activity and prints an alert when triggered.

        Checks failed login counts by IP address against the configured brute-force
        threshold. Alerts are only printed once per IP address to prevent duplicate
        alert spam during live monitoring.

        Args:
            analyser: Log analyser instance containing live failed IP counts.

        Returns:
            None
        """

        threshold = self.brute_force_threshold

        for (service, ip), attempts in analyser.failed_service_ip_counts.items():
            
            alert_key = f"{service}:{ip}"

            if (
                attempts >= threshold 
                and not self.has_alerted(BRUTE_FORCE_ALERT, alert_key)
            ):

                print_alert(
                    severity="HIGH",
                    title="Brute Force Detected",
                    message=(
                        f"Service: {service} | "
                        f"IP: {ip} | "
                        f"Attempts: {attempts}\n"
                    )
                )

                self.mark_alerted(
                    BRUTE_FORCE_ALERT,
                    alert_key
                )

    def detect_live_suspicious_success(
            self,
            analyser
        ) -> None:
        """
        Detects live successful logins from service/IP pairs that previously failed
        authentication.

        If a successful login comes from the same service and IP address as a previous
        failed login, a suspicious-success alert is printed. Each service/IP pair only
        triggers this alert once during the live session.

        Args:
            analyser: Log analyser instance containing live failed and successful
            login entries.

        Returns:
            None
        """

        failed_service_ips = {
            (
                entry.service,
                entry.ip
            )
            for entry in analyser.failed_logins
        }

        for entry in analyser.successful_logins:

            service_ip_key = (
                entry.service,
                entry.ip
            )

            alert_key = f"{entry.service}:{entry.ip}"

            if (
                service_ip_key in failed_service_ips
                and not self.has_alerted(SUSPICIOUS_SUCCESS_ALERT, alert_key)
            ):
                
                print_alert(
                    severity="MEDIUM",
                    title="Suspicious Success Detected",
                    message=(
                        f"Service: {entry.service} | "
                        f"IP: {entry.ip} | "
                        f"User: {entry.user} | "
                        f"Successful login after failure\n"
                    )
                )

                self.mark_alerted(
                    SUSPICIOUS_SUCCESS_ALERT,
                    alert_key
                )

    def detect_live_user_targeting(
            self,
            analyser
        ) -> None:
        """
        Detects live distributed user-targeting activity.

        Builds a mapping of service/username pairs to unique attacking IP addresses.
        If a username is targeted by enough unique IPs within the same service, an
        alert is printed once for that service/user pair.

        Args:
            analyser: Log analyser instance containing live failed login entries.

        Returns:
            None
        """

        service_user_to_ips = defaultdict(set)

        for entry in analyser.failed_logins:

            service_user_key = (
                entry.service,
                entry.user
            )

            service_user_to_ips[service_user_key].add(
                entry.ip
            )

        for (
            service,
            user
        ), ips in service_user_to_ips.items():

            unique_ip_count = len(
                ips
            )

            alert_key = f"{service}:{user}"

            if (
                unique_ip_count >= self.user_targeting_threshold
                and not self.has_alerted(USER_TARGETING_ALERT, alert_key)
            ):
                
                print_alert(
                    severity="HIGH",
                    title="User Targeting Detected",
                    message=(
                        f"Service: {service} | "
                        f"User: {user} | "
                        f"Unique IPs: {unique_ip_count} | "
                        f"Threshold: {self.user_targeting_threshold}\n"
                    )
                )

                self.mark_alerted(
                    USER_TARGETING_ALERT,
                    alert_key
                )