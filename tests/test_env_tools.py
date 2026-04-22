from pathlib import Path
from agent_dev_toolkit.env_tools import parse_template_keys, init_env, doctor_env

def test_parse_template_keys():
    text = "# comment\nAPI_KEY=123\nDEBUG=true\n\nINVALID\n"
    assert parse_template_keys(text) == ["API_KEY", "DEBUG"]

def test_init_env(tmp_path: Path):
    t = tmp_path / ".env.example"
    e = tmp_path / ".env"
    t.write_text("A=1\nB=2\n", encoding="utf-8")
    ok, _ = init_env(t, e)
    assert ok and e.exists()

def test_doctor_missing(tmp_path: Path):
    t = tmp_path / ".env.example"
    e = tmp_path / ".env"
    t.write_text("A=1\nB=2\n", encoding="utf-8")
    e.write_text("A=1\n", encoding="utf-8")
    ok, msg = doctor_env(t, e)
    assert not ok and "Missing keys" in msg

def test_doctor_ok(tmp_path: Path):
    t = tmp_path / ".env.example"
    e = tmp_path / ".env"
    c = "A=1\nB=2\n"
    t.write_text(c, encoding="utf-8")
    e.write_text(c, encoding="utf-8")
    ok, _ = doctor_env(t, e)
    assert ok
