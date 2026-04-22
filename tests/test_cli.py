import json
from pathlib import Path

from agent_dev_toolkit.cli import main


def test_doctor_json_output_ok_with_allow_extra(tmp_path: Path, capsys):
    template = tmp_path / ".env.example"
    env_file = tmp_path / ".env"
    template.write_text("A=1\n", encoding="utf-8")
    env_file.write_text("A=1\nB=2\n", encoding="utf-8")

    exit_code = main(
        [
            "env",
            "doctor",
            "--template",
            str(template),
            "--env-file",
            str(env_file),
            "--allow-extra",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr().out.strip()
    payload = json.loads(captured)
    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["missing"] == []
    assert payload["extra"] == []
    assert payload["allow_extra"] is True


def test_doctor_json_output_failure(tmp_path: Path, capsys):
    template = tmp_path / ".env.example"
    env_file = tmp_path / ".env"
    template.write_text("A=1\nB=2\n", encoding="utf-8")
    env_file.write_text("A=1\n", encoding="utf-8")

    exit_code = main(
        [
            "env",
            "doctor",
            "--template",
            str(template),
            "--env-file",
            str(env_file),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr().out.strip()
    payload = json.loads(captured)
    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["missing"] == ["B"]


def test_doctor_json_strict_with_allow_extra_fails(tmp_path: Path, capsys):
    template = tmp_path / ".env.example"
    env_file = tmp_path / ".env"
    template.write_text("A=1\n", encoding="utf-8")
    env_file.write_text("A=1\nB=2\n", encoding="utf-8")

    exit_code = main(
        [
            "env",
            "doctor",
            "--template",
            str(template),
            "--env-file",
            str(env_file),
            "--allow-extra",
            "--strict",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr().out.strip()
    payload = json.loads(captured)
    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["extra"] == ["B"]
    assert payload["strict"] is True


def test_doctor_output_file_written(tmp_path: Path, capsys):
    template = tmp_path / ".env.example"
    env_file = tmp_path / ".env"
    output_file = tmp_path / "doctor.json"
    template.write_text("A=1\n", encoding="utf-8")
    env_file.write_text("A=1\n", encoding="utf-8")

    exit_code = main(
        [
            "env",
            "doctor",
            "--template",
            str(template),
            "--env-file",
            str(env_file),
            "--format",
            "json",
            "--output",
            str(output_file),
        ]
    )

    captured = capsys.readouterr().out.strip()
    file_text = output_file.read_text(encoding="utf-8").strip()
    assert exit_code == 0
    assert captured == file_text
