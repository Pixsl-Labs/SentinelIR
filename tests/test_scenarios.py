from app.generator.ssh_scenarios import (
    generate_ssh_brute_force_scenario,
    generate_ssh_mixed_attack_scenario,
    generate_ssh_normal_activity,
    generate_ssh_suspicious_success_scenario,
    generate_ssh_user_targeting_scenario
)

def test_brute_force_scenario_generates_expected_attempt_count():
    lines = generate_ssh_brute_force_scenario(attempts=5)

    assert len(lines) == 5
    assert all("Failed password" in line for line in lines)

def test_suspicious_success_scenario_ends_with_success():
    lines = generate_ssh_suspicious_success_scenario(failed_attempts=3)

    assert len(lines) == 4
    assert "Accepted password" in lines[-1]
    assert all("Failed password" in line for line in lines[:-1])

def test_user_targeting_scenario_generates_unique_ips():
    lines = generate_ssh_user_targeting_scenario(unique_ips=5)

    assert len(lines) == 5
    assert "10.20.0.1" in lines[0]
    assert "10.20.0.5" in lines[-1]

def test_normal_activity_generates_successful_logins():
    lines = generate_ssh_normal_activity(events=5)

    assert len(lines) == 5
    assert all("Accepted password" in line for line in lines)

def test_mixed_attack_scenario_contains_all_attack_types():
    lines = generate_ssh_mixed_attack_scenario()

    joined_lines = "\n".join(lines)

    assert "Failed password for root from 192.168.1.50" in joined_lines
    assert "Accepted password for deploy from 192.168.1.60" in joined_lines
    assert "Failed password for admin from 10.20.0.5" in joined_lines