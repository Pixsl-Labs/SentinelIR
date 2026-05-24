from colorama import Fore


def get_severity_colour(
    severity: str
) -> str:

    if severity == "HIGH":
        return Fore.LIGHTRED_EX

    elif severity == "MEDIUM":
        return Fore.YELLOW
    
    elif severity == "LOW":
        return Fore.GREEN

    return Fore.WHITE


def get_status_colour(
    status: str
) -> str:

    if status.upper() == "FAILED":
        return Fore.LIGHTRED_EX

    elif status.upper() == "SUCCESS":
        return Fore.GREEN

    return Fore.WHITE

def get_attempt_colour(
    count: int
) -> str:
    
    if count >= 15:
        return Fore.LIGHTRED_EX
    
    elif count >= 10:
        return Fore.RED
    
    elif count >= 5:
        return Fore.LIGHTYELLOW_EX
    
    return Fore.LIGHTGREEN_EX

def get_count_colour(
    count: int
) -> str:

    if count >= 20:
        return Fore.LIGHTRED_EX

    elif count >= 10:
        return Fore.YELLOW

    elif count >= 1:
        return Fore.CYAN

    return Fore.LIGHTBLACK_EX

def get_live_status_colour(
        label: str,
        value: int
) -> str:
    
    label = label.lower()

    if label == "events_processed":
        return Fore.CYAN
    
    if label == "failed_logins":
        return get_attempt_colour(value)
    
    if label == "successful_logins":
        return Fore.GREEN if value > 0 else Fore.LIGHTRED_EX
    
    if label == "unique_ips":
        return get_count_colour(value)
    
    if label == "alerts_raised":
        if value >= 3:
            return Fore.LIGHTRED_EX
        
        if value >= 1:
            return Fore.YELLOW
        return Fore.LIGHTBLACK_EX
    
    if label == "brute_force_alert":
        return get_count_colour(value)
    
    if label == "suspicious_success":
        return get_count_colour(value)
    
    if label == "user_targeting":
        return get_count_colour(value)
    
    return Fore.WHITE