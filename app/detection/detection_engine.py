from collections import defaultdict

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


class DetectionEngine:

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