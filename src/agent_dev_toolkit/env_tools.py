from pathlib import Path

def parse_template_keys(template_text: str) -> list[str]:
    keys = []
    for raw_line in template_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key:
            keys.append(key)
    return keys

def init_env(template_path: Path, output_path: Path, force: bool = False):
    if not template_path.exists():
        return False, f"Template not found: {template_path}"
    if output_path.exists() and not force:
        return False, f"{output_path} already exists. Use --force to overwrite."
    output_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    return True, f"Created {output_path} from {template_path}"

def doctor_env_report(
    template_path: Path,
    env_path: Path,
    allow_extra: bool = False,
    strict: bool = False,
):
    report = {
        "ok": False,
        "missing": [],
        "extra": [],
        "allow_extra": allow_extra,
        "strict": strict,
        "message": "",
    }
    if not template_path.exists():
        report["message"] = f"Template not found: {template_path}"
        return report
    if not env_path.exists():
        report["message"] = f"Env file not found: {env_path}. Run env init first."
        return report
    template_keys = set(parse_template_keys(template_path.read_text(encoding="utf-8")))
    env_keys = set(parse_template_keys(env_path.read_text(encoding="utf-8")))
    missing = sorted(template_keys - env_keys)
    extra = sorted(env_keys - template_keys)
    if allow_extra and not strict:
        extra = []
    report["missing"] = missing
    report["extra"] = extra
    if not missing and not extra:
        if allow_extra and not strict:
            report["ok"] = True
            report["message"] = "Environment looks good: no missing keys."
            return report
        report["ok"] = True
        report["message"] = "Environment looks good: no missing or extra keys."
        return report
    lines = ["Environment differences detected:"]
    if missing:
        lines.append("- Missing keys: " + ", ".join(missing))
    if extra:
        lines.append("- Extra keys: " + ", ".join(extra))
    report["message"] = "\n".join(lines)
    return report

def doctor_env(
    template_path: Path,
    env_path: Path,
    allow_extra: bool = False,
    strict: bool = False,
):
    report = doctor_env_report(
        template_path,
        env_path,
        allow_extra=allow_extra,
        strict=strict,
    )
    return report["ok"], report["message"]
