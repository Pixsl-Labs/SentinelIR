import pytest

from app.generator.ssh_scenarios import (
    generate_ssh_failed_scenario,
    generate_ssh_success_scenario,
    generate_ssh_brute_force_scenario,
    generate_ssh_suspicious_success_scenario,
    # generate_ssh_user_targeting_scenario,
    # generate_ssh_normal_activity,
    # generate_ssh_mixed_attack_scenario
)

from app.generator.ftp_scenarios import (
    generate_ftp_failed_scenario,
    generate_ftp_success_scenario,
    generate_anonymous_ftp_scenario,
    generate_ftp_brute_force_scenario,
    generate_ftp_suspicious_success_scenario,
    # generate_ftp_user_targeting_scenario,
    # generate_ftp_normal_activity,
    # generate_ftp_mixed_attack_scenario
)

from app.generator.http_scenarios import (
    generate_http_failed_scenario,
    generate_http_success_scenario,
    generate_http_brute_force_scenario,
    generate_http_suspicious_success_scenario,
    # generate_http_user_targeting_scenario,
    # generate_http_normal_activity,
    # generate_http_mixed_attack_scenario
)

from app.runtime.generator_selection import (
    generate_mixed_service_attack_scenario,
    generate_ssh_ftp_mixed_attack_scenario,
    generate_ssh_http_mixed_attack_scenario,
    generate_ftp_http_mixed_attack_scenario
)

@pytest.mark.parametrize(
    "scenario_function, expected_text",
    [
        (generate_ssh_failed_scenario, "Failed password"),
        (generate_ftp_failed_scenario, "FTP LOGIN FAILED"),
        (generate_http_failed_scenario, "401"),
    ]
)
def test_failed_login_scenarios_generate_single_failed_login(
        scenario_function,
        expected_text
    ):
    lines = scenario_function()

    assert len(lines) == 1
    assert expected_text in lines[0]

@pytest.mark.parametrize(
    "scenario_function, expected_text",
    [
        (generate_ssh_success_scenario, "Accepted password"),
        (generate_ftp_success_scenario, "FTP LOGIN SUCCESS"),
        (generate_http_success_scenario, "200"),
    ]
)
def test_failed_login_scenarios_generate_expected_attempt_count(
        scenario_function,
        expected_text
    ):
    lines = scenario_function()

    assert len(lines) == 1
    assert all(expected_text in line for line in lines)

@pytest.mark.parametrize(
    "scenario_function, attempts, expected_text",
    [
        (generate_ssh_brute_force_scenario, 5, "Failed password"),
        (generate_ftp_brute_force_scenario, 5, "FTP LOGIN FAILED"),
        (generate_http_brute_force_scenario, 5, "401"),
    ]
)
def test_brute_force_scenarios_generate_expected_attempt_count(
        scenario_function,
        attempts,
        expected_text
    ):
    lines = scenario_function(
        attempts=attempts
    )

    assert len(lines) == attempts
    assert all(expected_text in line for line in lines)

@pytest.mark.parametrize(
    "scenario_function, failed_text, success_text",
    [
        (
            generate_ssh_suspicious_success_scenario,
            "Failed password",
            "Accepted password"
        ),
        (
            generate_ftp_suspicious_success_scenario,
            "FTP LOGIN FAILED",
            "FTP LOGIN SUCCESS"
        ),
        (
            generate_http_suspicious_success_scenario,
            "401",
            "200"
        ),
    ]
)
def test_suspicious_success_scenarios_end_with_success(
        scenario_function,
        failed_text,
        success_text
    ):
    lines = scenario_function(
        failed_attempts=3
    )

    assert len(lines) == 4
    assert success_text in lines[-1]
    assert all(failed_text in line for line in lines[:-1])

@pytest.mark.parametrize(
    "scenario_function, expected_text",
    [
        (generate_ssh_failed_scenario, "Failed password"),
        (generate_ftp_failed_scenario, "FTP LOGIN FAILED"),
        (generate_http_failed_scenario, "401"),
    ]
)
def test_single_failed_scenarios_generate_failed_login(
        scenario_function,
        expected_text
    ):
    lines = scenario_function()

    assert len(lines) == 1
    assert expected_text in lines[0]

@pytest.mark.parametrize(
    "scenario_function, expected_text",
    [
        (generate_ssh_success_scenario, "Accepted password"),
        (generate_ftp_success_scenario, "FTP LOGIN SUCCESS"),
        (generate_http_success_scenario, "200"),
    ]
)
def test_single_success_scenarios_generate_successful_login(
        scenario_function,
        expected_text
    ):
    lines = scenario_function()

    assert len(lines) == 1
    assert expected_text in lines[0]

def test_anonymous_ftp_scenario_generates_anonymous_login():
    lines = generate_anonymous_ftp_scenario()

    assert len(lines) == 1
    assert "FTP LOGIN SUCCESS" in lines[0]
    assert "user=anonymous" in lines[0]

def test_mixed_service_attack_scenario_contains_ssh_ftp_and_http_lines():
    lines = generate_mixed_service_attack_scenario()

    assert any("sshd" in line for line in lines)
    assert any("FTP LOGIN" in line for line in lines)
    assert any("HTTP/1.1" in line for line in lines)

def test_mixed_service_attack_scenario_contains_failed_and_successful_activity():
    lines = generate_mixed_service_attack_scenario()

    assert any("Failed password" in line or "FTP LOGIN FAILED" in line or "401" in line for line in lines)
    assert any("Accepted password" in line or "FTP LOGIN SUCCESS" in line or "200" in line for line in lines)

def test_mixed_service_attack_scenario_generates_expected_line_count():
    lines = generate_mixed_service_attack_scenario()

    assert len(lines) > 0

def test_ssh_ftp_mixed_attack_scenario_contains_ssh_and_ftp_lines():
    lines = generate_ssh_ftp_mixed_attack_scenario()

    assert any("sshd" in line for line in lines)
    assert any("FTP LOGIN" in line for line in lines)
    assert not any("HTTP/1.1" in line for line in lines)

def test_ssh_http_mixed_attack_scenario_contains_ssh_and_http_lines():
    lines = generate_ssh_http_mixed_attack_scenario()

    assert any("sshd" in line for line in lines)
    assert any("HTTP/1.1" in line for line in lines)
    assert not any("FTP LOGIN" in line for line in lines)

def test_ftp_http_mixed_attack_scenario_contains_ftp_and_http_lines():
    lines = generate_ftp_http_mixed_attack_scenario()

    assert any("FTP LOGIN" in line for line in lines)
    assert any("HTTP/1.1" in line for line in lines)
    assert not any("sshd" in line for line in lines)
