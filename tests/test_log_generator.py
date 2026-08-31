from app.generator.log_generator import (
    write_lines_to_file,
    stream_lines_to_file
)

def test_write_lines_to_file_writes_all_lines(tmp_path):
    output_file = tmp_path / "generated.log"

    lines = [
        "Apr 12 2026 12:00:00 server sshd[123]: Failed password for root from 192.168.1.10 port 22 ssh2",
        "Apr 12 2026 12:00:01 server sshd[123]: Failed password for root from 192.168.1.10 port 22 ssh2",
        "Apr 12 2026 12:00:02 server sshd[123]: Failed password for root from 192.168.1.10 port 22 ssh2"
    ]

    write_lines_to_file(
        file_path=output_file,
        lines=lines,
        append=True
    )

    assert output_file.read_text().splitlines() == lines

def test_write_lines_to_file_appends_to_existing_file(tmp_path):
    output_file = tmp_path / "generated.log"

    old_lines = [
        "Apr 12 2026 12:00:02 server sshd[123]: Failed password for root from 192.168.1.10 port 22 ssh2"
    ]

    write_lines_to_file(
        file_path=output_file,
        lines=old_lines,
        append=False
    )

    new_lines = [
        "Apr 12 2026 12:00:00 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2",
        "Apr 12 2026 12:00:01 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2",
        "Apr 12 2026 12:00:02 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2"
    ]

    write_lines_to_file(
        file_path=output_file,
        lines=new_lines,
        append=True
    )

    lines_content = old_lines + new_lines

    assert output_file.read_text().splitlines() == lines_content

def test_write_lines_to_file_overwrites_existing_file(tmp_path):
    output_file = tmp_path / "generated.log"

    old_lines = [
        "Apr 12 2026 12:00:02 server sshd[123]: Failed password for root from 192.168.1.10 port 22 ssh2"
    ]

    write_lines_to_file(
        file_path=output_file,
        lines=old_lines,
        append=False
    )

    new_lines = [
        "Apr 12 2026 12:00:00 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2",
        "Apr 12 2026 12:00:01 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2",
        "Apr 12 2026 12:00:02 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2"
    ]

    write_lines_to_file(
        file_path=output_file,
        lines=new_lines,
        append=False
    )

    assert output_file.read_text().splitlines() == new_lines

def test_stream_lines_to_file_writes_all_lines(tmp_path):
    output_file = tmp_path / "generated.log"

    lines = [
        "Apr 12 2026 12:00:00 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2",
        "Apr 12 2026 12:00:01 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2",
        "Apr 12 2026 12:00:02 server sshd[123]: Failed password for root from 192.168.1.20 port 22 ssh2"
    ]

    stream_lines_to_file(
        file_path=output_file,
        lines=lines,
        delay_seconds=0
    )

    assert output_file.read_text().splitlines() == lines
